import json
import re
from functools import wraps

from django.contrib import messages
from django.db import transaction
from django.db.models import Prefetch
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST

from core.ratelimit import ratelimit

from . import engine
from .models import Attempt, Exam, MockTest, Option, Plan, Response

NAME_RE = re.compile(r"^[A-Za-z][A-Za-z .'-]{1,59}$")


def _session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def _owned_attempts(request):
    if request.user.is_authenticated:
        return Attempt.objects.filter(user=request.user)
    return Attempt.objects.filter(session_key=_session_key(request), user__isnull=True)


def _get_attempt(request, attempt_id):
    try:
        return _owned_attempts(request).select_related('mock__exam').get(pk=attempt_id)
    except Attempt.DoesNotExist:
        raise Http404


# ------------------------------------------------------------------ pages

@require_GET
def exam_detail(request, slug):
    exam = get_object_or_404(Exam, slug=slug)
    mocks = exam.mocks.filter(is_published=True).prefetch_related('sections__questions')
    return render(request, 'exams/exam_detail.html', {
        'exam': exam,
        'mocks': mocks,
        'plan': Plan.objects.filter(exam=exam, is_active=True).first(),
    })


def instructions(request, slug):
    mock = get_object_or_404(
        MockTest.objects.select_related('exam').prefetch_related('sections__questions'),
        slug=slug, is_published=True,
    )
    if not mock.is_free:
        messages.info(request, f'{mock.title} is part of the Pro pack. Unlock it to attempt.')
        return redirect(reverse('exam_detail', args=[mock.exam.slug]) + '#pricing')

    in_progress = _owned_attempts(request).filter(mock=mock, status=Attempt.IN_PROGRESS).first()
    if in_progress:
        engine.sync(in_progress)
        if in_progress.is_submitted:
            in_progress = None

    error = None
    if request.method == 'POST':
        name = ' '.join(request.POST.get('candidate_name', '').split())
        if not request.POST.get('declaration'):
            error = 'Please accept the declaration to begin.'
        elif not NAME_RE.match(name):
            error = 'Enter your name using letters only (2–60 characters).'
        elif in_progress:
            return redirect('attempt', in_progress.pk)
        else:
            attempt = engine.create_attempt(
                mock,
                session_key=_session_key(request),
                candidate_name=name,
                user=request.user if request.user.is_authenticated else None,
            )
            return redirect('attempt', attempt.pk)

    request.no_store = True
    return render(request, 'exams/instructions.html', {
        'mock': mock,
        'sections': mock.sections.all(),
        'in_progress': in_progress,
        'error': error,
        'step': 2 if request.method == 'POST' else 1,
    })


@require_GET
def attempt_page(request, attempt_id):
    attempt = _get_attempt(request, attempt_id)
    with transaction.atomic():
        attempt = engine.lock(attempt.pk)
        engine.sync(attempt)
        if attempt.is_submitted:
            return redirect('result', attempt.pk)
        token = engine.issue_window_token(attempt)
    sections = engine.sections_of(attempt)
    return render(request, 'exams/attempt.html', {
        'attempt': attempt,
        'mock': attempt.mock,
        'config': {
            'token': token,
            'candidate': attempt.candidate_name,
            'attemptId': attempt.short_id,
            'title': attempt.mock.title,
            'urls': {
                'state': reverse('api_state', args=[attempt.pk]),
                'question': reverse('api_question', args=[attempt.pk]),
                'answer': reverse('api_answer', args=[attempt.pk]),
                'event': reverse('api_event', args=[attempt.pk]),
                'summary': reverse('api_summary', args=[attempt.pk]),
                'submit': reverse('api_submit', args=[attempt.pk]),
                'result': reverse('result', args=[attempt.pk]),
            },
            'sectionNames': [s.name for s in sections],
        },
    })


@require_GET
def result(request, attempt_id):
    attempt = _get_attempt(request, attempt_id)
    if not attempt.is_submitted:
        with transaction.atomic():
            attempt = engine.sync(engine.lock(attempt.pk))
        if not attempt.is_submitted:
            return redirect('attempt', attempt.pk)

    responses = list(attempt.responses.select_related('question__section', 'selected'))
    sections = []
    for s in engine.sections_of(attempt):
        rs = [r for r in responses if r.question.section_id == s.pk]
        attempted = [r for r in rs if r.counts_as_answer]
        correct = sum(1 for r in attempted if r.selected.is_correct)
        wrong = len(attempted) - correct
        score = correct * attempt.mock.positive_marks - wrong * attempt.mock.negative_marks
        sections.append({
            'name': s.name,
            'total': len(rs),
            'attempted': len(attempted),
            'correct': correct,
            'wrong': wrong,
            'skipped': len(rs) - len(attempted),
            'score': score,
            'accuracy': round(100 * correct / len(attempted)) if attempted else 0,
            'seconds': sum(r.seconds_spent for r in rs),
            'minutes': s.duration_minutes,
            'score_pct': max(0, float(score)) * 100 / len(rs) if rs else 0,
        })
    attempted = attempt.correct + attempt.wrong
    total = len(responses)
    request.no_store = True
    return render(request, 'exams/result.html', {
        'attempt': attempt,
        'mock': attempt.mock,
        'sections': sections,
        'total': total,
        'attempted': attempted,
        'accuracy': round(100 * attempt.correct / attempted) if attempted else 0,
        'negative': attempt.wrong * attempt.mock.negative_marks,
        'score_pct': max(0, float(attempt.score)) * 100 / total if total else 0,
        'seconds': sum(r.seconds_spent for r in responses),
        'plan': Plan.objects.filter(exam=attempt.mock.exam, is_active=True).first(),
        'pro_count': attempt.mock.exam.mocks.filter(is_published=True, is_free=False).count(),
    })


@require_GET
def solutions(request, attempt_id):
    attempt = _get_attempt(request, attempt_id)
    if not attempt.is_submitted:
        raise Http404
    responses = (
        attempt.responses
        .select_related('question__section', 'question__passage', 'selected')
        .prefetch_related(Prefetch('question__options', queryset=Option.objects.order_by('order')))
    )
    sections = []
    for s in engine.sections_of(attempt):
        sections.append({
            'name': s.name,
            'responses': [r for r in responses if r.question.section_id == s.pk],
        })
    request.no_store = True
    return render(request, 'exams/solutions.html', {
        'attempt': attempt,
        'mock': attempt.mock,
        'sections': sections,
        'Response': Response,
    })


# -------------------------------------------------------------------- API

def exam_api(view):
    """POST-only JSON endpoint bound to the attempt owner *and* the active window."""

    @require_POST
    @wraps(view)
    def wrapped(request, attempt_id):
        attempt = _get_attempt(request, attempt_id)
        try:
            payload = json.loads(request.body or b'{}')
            if not isinstance(payload, dict):
                raise ValueError
        except ValueError:
            return JsonResponse({'error': 'bad_request'}, status=400)
        request.no_store = True
        try:
            with transaction.atomic():
                attempt = engine.lock(attempt.pk)
                engine.sync(attempt)
                if attempt.is_submitted:
                    return JsonResponse(
                        {'error': 'submitted', 'redirect': reverse('result', args=[attempt.pk])},
                        status=409,
                    )
                engine.check_window(attempt, request.headers.get('X-Exam-Window', ''))
                return view(request, attempt, payload)
        except engine.ExamError as e:
            return JsonResponse({'error': e.code}, status=e.status)

    return wrapped


def _with_state(attempt, data=None):
    body = {'state': engine.state(attempt)}
    if attempt.is_submitted:
        body['redirect'] = reverse('result', args=[attempt.pk])
    if data:
        body.update(data)
    return JsonResponse(body)


@ratelimit('state', 60)
@exam_api
def api_state(request, attempt, payload):
    return _with_state(attempt)


@ratelimit('question', 90)
@exam_api
def api_question(request, attempt, payload):
    response = engine.visit(attempt, payload.get('n'))
    return _with_state(attempt, {'question': engine.question_payload(attempt, response)})


@ratelimit('answer', 120)
@exam_api
def api_answer(request, attempt, payload):
    option = payload.get('option')
    if option is not None and not isinstance(option, int):
        return JsonResponse({'error': 'bad_option'}, status=400)
    engine.answer(attempt, payload.get('n'), payload.get('action'), option)
    return _with_state(attempt)


@ratelimit('event', 60)
@exam_api
def api_event(request, attempt, payload):
    engine.record_event(attempt, str(payload.get('kind', ''))[:30], ip=request.META.get('REMOTE_ADDR'))
    return _with_state(attempt)


@ratelimit('summary', 30)
@exam_api
def api_summary(request, attempt, payload):
    return _with_state(attempt, {'summary': engine.summary(attempt)})


@ratelimit('submit', 10)
@exam_api
def api_submit(request, attempt, payload):
    engine.submit(attempt)
    return _with_state(attempt)
