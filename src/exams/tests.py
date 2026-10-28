import io
import json
import re
from datetime import timedelta
from decimal import Decimal
from unittest import mock

from django.core.cache import cache
from django.core.management import call_command
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from . import engine
from .models import Attempt, MockTest, Option, Response

FREE_SLUG = 'ibps-po-prelims-free-mock-1'


class ExamTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_mocks', stdout=io.StringIO())
        cls.mock = MockTest.objects.get(slug=FREE_SLUG)

    def setUp(self):
        cache.clear()
        self.client = Client()

    def start(self, client=None, name='Priya Sharma'):
        client = client or self.client
        res = client.post(reverse('instructions', args=[FREE_SLUG]),
                          {'candidate_name': name, 'declaration': '1'})
        self.assertEqual(res.status_code, 302)
        attempt = Attempt.objects.latest('started_at')
        page = client.get(reverse('attempt', args=[attempt.pk]))
        config = json.loads(re.search(
            r'<script id="exam-config" type="application/json">(.*?)</script>',
            page.content.decode(), re.S).group(1))
        return attempt, config

    def call(self, config, name, body=None, token=None, client=None):
        client = client or self.client
        return client.post(
            config['urls'][name], data=json.dumps(body or {}), content_type='application/json',
            headers={'X-Exam-Window': config['token'] if token is None else token},
        )

    def rewind(self, attempt, minutes):
        Attempt.objects.filter(pk=attempt.pk).update(
            started_at=attempt.started_at - timedelta(minutes=minutes),
            section_started_at=attempt.section_started_at - timedelta(minutes=minutes),
        )


class SeedTests(ExamTestCase):
    def test_pattern_matches_ibps_po_prelims(self):
        sections = list(self.mock.sections.all())
        self.assertEqual([(s.name, s.questions.count(), s.duration_minutes) for s in sections], [
            ('English Language', 30, 20),
            ('Quantitative Aptitude', 35, 20),
            ('Reasoning Ability', 35, 20),
        ])

    def test_every_question_has_exactly_one_correct_option(self):
        for q in self.mock.sections.first().questions.model.objects.filter(section__mock=self.mock):
            self.assertEqual(q.options.filter(is_correct=True).count(), 1, q)
            self.assertEqual(q.options.count(), 5, q)


class PageTests(ExamTestCase):
    def test_public_pages_render(self):
        for url in [reverse('home'), reverse('exam_detail', args=['ibps-po']),
                    reverse('instructions', args=[FREE_SLUG])]:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 200, url)
        self.assertContains(self.client.get(reverse('home')), 'MeritMocks')

    def test_security_headers(self):
        res = self.client.get(reverse('home'))
        self.assertIn("script-src 'self'", res['Content-Security-Policy'])
        self.assertIn("frame-ancestors 'none'", res['Content-Security-Policy'])
        self.assertEqual(res['X-Frame-Options'], 'DENY')
        self.assertIn('camera=()', res['Permissions-Policy'])

    def test_pro_mock_is_locked(self):
        res = self.client.get(reverse('instructions', args=['ibps-po-prelims-mock-2']))
        self.assertRedirects(res, reverse('exam_detail', args=['ibps-po']) + '#pricing',
                             fetch_redirect_response=False)

    def test_start_requires_declaration_and_valid_name(self):
        url = reverse('instructions', args=[FREE_SLUG])
        self.assertContains(self.client.post(url, {'candidate_name': 'Priya'}), 'accept the declaration')
        self.assertContains(self.client.post(url, {'candidate_name': '<script>', 'declaration': '1'}),
                            'letters only')
        self.assertFalse(Attempt.objects.exists())


class AttemptAccessTests(ExamTestCase):
    def test_exam_pages_are_not_cached(self):
        attempt, _ = self.start()
        res = self.client.get(reverse('attempt', args=[attempt.pk]))
        self.assertIn('no-store', res['Cache-Control'])

    def test_other_session_cannot_see_attempt(self):
        attempt, config = self.start()
        intruder = Client()
        self.assertEqual(intruder.get(reverse('attempt', args=[attempt.pk])).status_code, 404)
        self.assertEqual(self.call(config, 'state', client=intruder).status_code, 404)

    def test_api_requires_active_window_token(self):
        attempt, config = self.start()
        res = self.call(config, 'state', token='forged')
        self.assertEqual(res.status_code, 409)
        self.assertEqual(res.json()['error'], 'another_window')

    def test_opening_second_window_locks_the_first(self):
        attempt, first = self.start()
        self.client.get(reverse('attempt', args=[attempt.pk]))  # reopen in a new tab
        self.assertEqual(self.call(first, 'state').json()['error'], 'another_window')

    def test_api_rejects_get_and_missing_csrf(self):
        attempt, config = self.start()
        self.assertEqual(self.client.get(config['urls']['state']).status_code, 405)
        strict = Client(enforce_csrf_checks=True)
        strict.cookies = self.client.cookies
        self.assertEqual(self.call(config, 'state', client=strict).status_code, 403)


class ExamFlowTests(ExamTestCase):
    def test_question_payload_never_reveals_answers(self):
        attempt, config = self.start()
        res = self.call(config, 'question', {'n': 1})
        self.assertEqual(res.status_code, 200)
        raw = res.content.decode()
        for leak in ('is_correct', 'explanation', 'correct'):
            self.assertNotIn(leak, raw)
        self.assertEqual(len(res.json()['question']['options']), 5)

    def test_cannot_open_questions_of_other_sections(self):
        attempt, config = self.start()
        res = self.call(config, 'question', {'n': 31})
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.json()['error'], 'section_locked')

    def test_statuses_follow_tcs_rules(self):
        attempt, config = self.start()
        self.call(config, 'question', {'n': 1})
        self.call(config, 'answer', {'n': 1, 'action': 'save', 'option': 2})
        self.call(config, 'question', {'n': 2})
        self.call(config, 'answer', {'n': 2, 'action': 'mark', 'option': None})
        self.call(config, 'question', {'n': 3})
        self.call(config, 'answer', {'n': 3, 'action': 'mark', 'option': 1})
        self.call(config, 'question', {'n': 4})
        palette = {p['n']: p['s'] for p in self.call(config, 'state').json()['state']['palette']}
        self.assertEqual(palette[1], 'answered')
        self.assertEqual(palette[2], 'marked')
        self.assertEqual(palette[3], 'answered_marked')
        self.assertEqual(palette[4], 'not_answered')
        self.assertEqual(palette[5], 'not_visited')
        self.call(config, 'answer', {'n': 1, 'action': 'clear'})
        self.assertEqual(attempt.responses.get(number=1).status, Response.NOT_ANSWERED)

    def test_section_advances_on_server_clock_and_locks(self):
        attempt, config = self.start()
        self.rewind(attempt, 21)
        state = self.call(config, 'state').json()['state']
        self.assertEqual(state['section_index'], 1)
        self.assertLessEqual(state['remaining'], 19 * 60)
        self.assertEqual(state['palette'][0]['n'], 31)
        res = self.call(config, 'answer', {'n': 1, 'action': 'save', 'option': 0})
        self.assertEqual(res.status_code, 403)

    def test_submit_only_in_last_section(self):
        attempt, config = self.start()
        res = self.call(config, 'submit')
        self.assertEqual(res.json()['error'], 'not_last_section')
        self.rewind(attempt, 41)
        res = self.call(config, 'submit')
        self.assertEqual(res.status_code, 200)
        self.assertIn('redirect', res.json())

    def test_time_up_auto_submits_and_scores(self):
        attempt, config = self.start()
        correct = Option.objects.get(question__section__mock=self.mock, question__order=1,
                                     question__section__order=1, is_correct=True)
        wrong = Option.objects.filter(question__section__mock=self.mock, question__order=2,
                                      question__section__order=1, is_correct=False).first()
        self.call(config, 'question', {'n': 1})
        self.call(config, 'answer', {'n': 1, 'action': 'save', 'option': correct.order})
        self.call(config, 'question', {'n': 2})
        self.call(config, 'answer', {'n': 2, 'action': 'mark', 'option': wrong.order})
        self.rewind(attempt, 61)
        res = self.call(config, 'state')
        self.assertEqual(res.status_code, 409)
        attempt.refresh_from_db()
        self.assertEqual(attempt.status, Attempt.SUBMITTED)
        self.assertEqual(attempt.submit_reason, Attempt.BY_TIMEOUT)
        self.assertEqual((attempt.correct, attempt.wrong), (1, 1))
        self.assertEqual(attempt.score, Decimal('0.75'))
        self.assertEqual(self.client.get(reverse('result', args=[attempt.pk])).status_code, 200)
        self.assertContains(self.client.get(reverse('solutions', args=[attempt.pk])), 'Correct answer')

    def test_late_answer_after_deadline_is_rejected(self):
        attempt, config = self.start()
        self.call(config, 'question', {'n': 1})
        attempt.refresh_from_db()
        with self.assertRaises(engine.ExamError) as ctx:
            engine.answer(attempt, 1, 'save', 0,
                          now=attempt.section_started_at + timedelta(minutes=20, seconds=10))
        self.assertEqual(ctx.exception.code, 'section_closed')

    def test_solutions_hidden_until_submitted(self):
        attempt, _ = self.start()
        self.assertEqual(self.client.get(reverse('solutions', args=[attempt.pk])).status_code, 404)

    def test_time_spent_is_measured_by_server(self):
        attempt, config = self.start()
        self.call(config, 'question', {'n': 1})
        Attempt.objects.filter(pk=attempt.pk).update(
            current_question_since=timezone.now() - timedelta(seconds=42))
        self.call(config, 'question', {'n': 2})
        self.assertGreaterEqual(attempt.responses.get(number=1).seconds_spent, 42)


class ProctoringTests(ExamTestCase):
    def test_violations_auto_submit(self):
        attempt, config = self.start()
        with mock.patch.object(engine, 'EVENT_DEBOUNCE', timedelta(0)):
            for i in range(self.mock.max_warnings - 1):
                state = self.call(config, 'event', {'kind': 'focus_lost'}).json()['state']
                self.assertEqual(state['warnings'], i + 1)
            res = self.call(config, 'event', {'kind': 'fullscreen_exit'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('redirect', res.json())
        attempt.refresh_from_db()
        self.assertEqual(attempt.submit_reason, Attempt.BY_VIOLATIONS)

    def test_rapid_duplicate_focus_events_count_once(self):
        attempt, config = self.start()
        self.call(config, 'event', {'kind': 'focus_lost'})
        state = self.call(config, 'event', {'kind': 'fullscreen_exit'}).json()['state']
        self.assertEqual(state['warnings'], 1)

    def test_copy_attempts_are_logged_but_not_counted(self):
        attempt, config = self.start()
        state = self.call(config, 'event', {'kind': 'copy'}).json()['state']
        self.assertEqual(state['warnings'], 0)
        self.assertTrue(attempt.events.filter(kind='copy').exists())
        self.assertEqual(self.call(config, 'event', {'kind': 'nonsense'}).status_code, 400)

    def test_question_endpoint_is_rate_limited(self):
        attempt, config = self.start()
        codes = [self.call(config, 'question', {'n': 1 + i % 30}).status_code for i in range(95)]
        self.assertIn(429, codes)
