"""Server-authoritative exam engine.

The browser only *displays* the clock. Every deadline is derived from
timestamps stored here, so pausing JavaScript, changing the system clock,
sleeping the laptop or editing the page cannot buy extra time. Correct answers
never leave the server until the attempt is submitted.
"""

import secrets
from datetime import timedelta

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import Attempt, Option, ProctorEvent, Question, Response

# Answers that were in flight when the clock hit zero are still accepted.
NETWORK_GRACE = timedelta(seconds=3)
COUNTED_EVENTS = {'focus_lost', 'fullscreen_exit'}
LOGGED_EVENTS = COUNTED_EVENTS | {
    'copy', 'paste', 'context_menu', 'print', 'print_screen', 'devtools_key', 'select_all',
}
# Switching tabs fires blur + visibilitychange back to back; count it once.
EVENT_DEBOUNCE = timedelta(seconds=3)


class ExamError(Exception):
    def __init__(self, code, status=409):
        super().__init__(code)
        self.code = code
        self.status = status


def sections_of(attempt):
    return list(attempt.mock.sections.all())


def current_section(attempt):
    return sections_of(attempt)[attempt.section_index]


def section_deadline(attempt):
    return attempt.section_started_at + current_section(attempt).duration


def remaining_seconds(attempt, now=None):
    if attempt.is_submitted:
        return 0
    now = now or timezone.now()
    return max(0, int((section_deadline(attempt) - now).total_seconds()))


def create_attempt(mock, *, session_key, candidate_name, user=None):
    now = timezone.now()
    with transaction.atomic():
        attempt = Attempt.objects.create(
            mock=mock,
            user=user,
            session_key=session_key,
            candidate_name=candidate_name,
            started_at=now,
            section_started_at=now,
        )
        questions = Question.objects.filter(section__mock=mock).order_by('section__order', 'order')
        Response.objects.bulk_create(
            Response(attempt=attempt, question=q, number=n)
            for n, q in enumerate(questions, start=1)
        )
    return attempt


def lock(attempt_id):
    """Re-read the attempt under a row lock; call inside transaction.atomic()."""
    return Attempt.objects.select_for_update().select_related('mock').get(pk=attempt_id)


def _credit_time(attempt, until):
    if not (attempt.current_question_id and attempt.current_question_since):
        return
    seconds = int((until - attempt.current_question_since).total_seconds())
    if seconds > 0:
        Response.objects.filter(attempt=attempt, question_id=attempt.current_question_id).update(
            seconds_spent=F('seconds_spent') + seconds
        )
        # Carry the fractional remainder forward so quick navigation is not lost.
        attempt.current_question_since += timedelta(seconds=seconds)


def sync(attempt, now=None):
    """Advance past every section whose time is over; submit after the last one."""
    if attempt.is_submitted:
        return attempt
    now = now or timezone.now()
    sections = sections_of(attempt)
    changed = False
    while True:
        deadline = attempt.section_started_at + sections[attempt.section_index].duration
        if now < deadline:
            break
        _credit_time(attempt, deadline)
        if attempt.section_index + 1 >= len(sections):
            finalize(attempt, Attempt.BY_TIMEOUT, at=deadline)
            return attempt
        attempt.section_index += 1
        attempt.section_started_at = deadline
        attempt.current_question = None
        attempt.current_question_since = None
        changed = True
    if changed:
        attempt.save()
    return attempt


def finalize(attempt, reason, at=None):
    if attempt.is_submitted:
        return attempt
    at = min(at or timezone.now(), timezone.now())
    _credit_time(attempt, at)
    correct = wrong = 0
    for r in attempt.responses.select_related('selected'):
        if r.counts_as_answer:
            if r.selected.is_correct:
                correct += 1
            else:
                wrong += 1
    mock = attempt.mock
    attempt.correct = correct
    attempt.wrong = wrong
    attempt.score = correct * mock.positive_marks - wrong * mock.negative_marks
    attempt.status = Attempt.SUBMITTED
    attempt.submit_reason = reason
    attempt.submitted_at = at
    attempt.current_question = None
    attempt.current_question_since = None
    attempt.window_token = ''
    attempt.save()
    return attempt


def issue_window_token(attempt):
    """Bind the attempt to the window that just opened it; older windows lose access."""
    attempt.window_token = secrets.token_urlsafe(24)
    attempt.save(update_fields=['window_token'])
    return attempt.window_token


def check_window(attempt, token):
    if attempt.is_submitted:
        raise ExamError('submitted')
    if not token or not secrets.compare_digest(attempt.window_token, token):
        raise ExamError('another_window')


def _response_in_current_section(attempt, number):
    try:
        response = attempt.responses.select_related('question__passage', 'selected').get(
            number=number
        )
    except (Response.DoesNotExist, ValueError, TypeError):
        raise ExamError('no_such_question', status=404)
    if response.question.section_id != current_section(attempt).pk:
        raise ExamError('section_locked', status=403)
    return response


def visit(attempt, number, now=None):
    now = now or timezone.now()
    response = _response_in_current_section(attempt, number)
    if attempt.current_question_id != response.question_id:
        _credit_time(attempt, now)
        attempt.current_question = response.question
        attempt.current_question_since = now
        attempt.save(update_fields=['current_question', 'current_question_since'])
    if response.status == Response.NOT_VISITED:
        response.status = Response.NOT_ANSWERED
        response.save(update_fields=['status'])
    return response


def answer(attempt, number, action, option_index, now=None):
    now = now or timezone.now()
    if now > section_deadline(attempt) + NETWORK_GRACE:
        raise ExamError('section_closed')
    response = _response_in_current_section(attempt, number)
    option = None
    if action != 'clear' and option_index is not None:
        option = Option.objects.filter(question=response.question, order=option_index).first()
        if option is None:
            raise ExamError('bad_option', status=400)

    if action == 'clear':
        response.selected, response.status = None, Response.NOT_ANSWERED
    elif action == 'mark':
        response.selected = option
        response.status = Response.ANSWERED_MARKED if option else Response.MARKED
    elif action == 'save':
        response.selected = option
        response.status = Response.ANSWERED if option else Response.NOT_ANSWERED
    else:
        raise ExamError('bad_action', status=400)
    response.save(update_fields=['selected', 'status'])
    return response


def record_event(attempt, kind, ip=None, now=None):
    """Log a proctoring event; returns True if the attempt was auto-submitted."""
    if kind not in LOGGED_EVENTS:
        raise ExamError('bad_event', status=400)
    now = now or timezone.now()
    counted = False
    if kind in COUNTED_EVENTS:
        last = attempt.events.filter(counted=True).first()
        counted = last is None or now - last.created_at > EVENT_DEBOUNCE
    ProctorEvent.objects.create(attempt=attempt, kind=kind, counted=counted, ip=ip)
    if counted:
        attempt.warnings += 1
        attempt.save(update_fields=['warnings'])
        limit = attempt.mock.max_warnings
        if limit and attempt.warnings >= limit:
            finalize(attempt, Attempt.BY_VIOLATIONS, at=now)
            return True
    return False


def submit(attempt):
    if attempt.section_index != len(sections_of(attempt)) - 1:
        raise ExamError('not_last_section', status=403)
    return finalize(attempt, Attempt.BY_CANDIDATE)


# ---------------------------------------------------------------- serializers

def palette(attempt):
    section = current_section(attempt)
    return [
        {'n': r.number, 's': r.status}
        for r in attempt.responses.filter(question__section=section).only('number', 'status')
    ]


def state(attempt):
    sections = sections_of(attempt)
    counts = {s.pk: s.questions.count() for s in sections}
    return {
        'status': attempt.status,
        'section_index': attempt.section_index,
        'sections': [
            {
                'name': s.name,
                'count': counts[s.pk],
                'minutes': s.duration_minutes,
                'state': 'done' if i < attempt.section_index
                else 'active' if i == attempt.section_index else 'upcoming',
            }
            for i, s in enumerate(sections)
        ],
        'remaining': remaining_seconds(attempt),
        'palette': palette(attempt) if not attempt.is_submitted else [],
        'current': (
            attempt.responses.filter(question_id=attempt.current_question_id)
            .values_list('number', flat=True).first()
            if attempt.current_question_id else None
        ),
        'warnings': attempt.warnings,
        'max_warnings': attempt.mock.max_warnings,
    }


def question_payload(attempt, response):
    q = response.question
    passage = q.passage
    options = list(q.options.all())
    selected_index = next((o.order for o in options if o.pk == response.selected_id), None)
    return {
        'n': response.number,
        'status': response.status,
        'text': q.text,
        'options': [{'i': o.order, 'text': o.text} for o in options],
        'selected': selected_index,
        'passage': {
            'id': passage.pk,
            'directions': passage.directions,
            'body': passage.body,
            'layout': passage.layout,
        } if passage else None,
        'marks': {
            'positive': str(attempt.mock.positive_marks.normalize()),
            'negative': str(attempt.mock.negative_marks.normalize()),
        },
    }


def summary(attempt):
    rows = []
    for s in sections_of(attempt):
        rs = list(attempt.responses.filter(question__section=s).values_list('status', flat=True))
        rows.append({
            'name': s.name,
            'total': len(rs),
            **{key: rs.count(key) for key, _ in Response.STATUSES},
        })
    return rows
