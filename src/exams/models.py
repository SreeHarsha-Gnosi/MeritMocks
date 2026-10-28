import uuid
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models


class ExamCategory(models.Model):
    """Banking, Insurance, Regulatory bodies, Government."""

    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=160, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'exam categories'

    def __str__(self):
        return self.name


class Exam(models.Model):
    category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=120)
    short_name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)
    conducting_body = models.CharField(max_length=120, blank=True)
    is_live = models.BooleanField(default=False, help_text='Has published mocks users can take.')
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.short_name


class MockTest(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='mocks')
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    stage = models.CharField(max_length=40, default='Prelims')
    is_free = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    positive_marks = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('1'))
    negative_marks = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.25'))
    max_warnings = models.PositiveSmallIntegerField(
        default=5,
        help_text='Auto-submit after this many focus/fullscreen violations. 0 disables.',
    )

    class Meta:
        ordering = ['exam', 'order']

    def __str__(self):
        return self.title

    @property
    def total_questions(self):
        return sum(s.questions.count() for s in self.sections.all())

    @property
    def total_minutes(self):
        return sum(s.duration_minutes for s in self.sections.all())

    @property
    def max_marks(self):
        return self.total_questions * self.positive_marks


class Section(models.Model):
    mock = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=80)
    order = models.PositiveSmallIntegerField(default=0)
    duration_minutes = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['mock', 'order']

    def __str__(self):
        return f'{self.mock} · {self.name}'

    @property
    def duration(self):
        return timedelta(minutes=self.duration_minutes)


class Passage(models.Model):
    """Shared directions/content for a group of questions (RC, DI, puzzles...)."""

    SPLIT = 'split'
    INLINE = 'inline'
    LAYOUTS = [(SPLIT, 'Side by side'), (INLINE, 'Above question')]

    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='passages')
    directions = models.TextField(help_text='Trusted HTML written by staff.')
    body = models.TextField(blank=True, help_text='Trusted HTML written by staff.')
    layout = models.CharField(max_length=10, choices=LAYOUTS, default=SPLIT)

    def __str__(self):
        return self.directions[:60]


class Question(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='questions')
    passage = models.ForeignKey(
        Passage, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions'
    )
    order = models.PositiveSmallIntegerField()
    text = models.TextField(help_text='Trusted HTML written by staff.')
    explanation = models.TextField(blank=True, help_text='Trusted HTML written by staff.')
    topic = models.CharField(max_length=60, blank=True)

    class Meta:
        ordering = ['section__order', 'order']
        constraints = [
            models.UniqueConstraint(fields=['section', 'order'], name='unique_question_order'),
        ]

    def __str__(self):
        return f'{self.section.name} Q{self.order}'


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    order = models.PositiveSmallIntegerField()
    text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Plan(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='plans')
    name = models.CharField(max_length=80)
    price_inr = models.PositiveIntegerField()
    mrp_inr = models.PositiveIntegerField(null=True, blank=True)
    features = models.TextField(help_text='One feature per line.')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class Attempt(models.Model):
    IN_PROGRESS = 'in_progress'
    SUBMITTED = 'submitted'
    STATUSES = [(IN_PROGRESS, 'In progress'), (SUBMITTED, 'Submitted')]

    BY_CANDIDATE = 'candidate'
    BY_TIMEOUT = 'time_up'
    BY_VIOLATIONS = 'violations'
    SUBMIT_REASONS = [
        (BY_CANDIDATE, 'Submitted by candidate'),
        (BY_TIMEOUT, 'Time up'),
        (BY_VIOLATIONS, 'Auto-submitted for violations'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mock = models.ForeignKey(MockTest, on_delete=models.PROTECT, related_name='attempts')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    session_key = models.CharField(max_length=64, db_index=True)
    candidate_name = models.CharField(max_length=60)
    status = models.CharField(max_length=20, choices=STATUSES, default=IN_PROGRESS)
    submit_reason = models.CharField(max_length=20, choices=SUBMIT_REASONS, blank=True)

    started_at = models.DateTimeField()
    section_index = models.PositiveSmallIntegerField(default=0)
    section_started_at = models.DateTimeField()
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    current_question_since = models.DateTimeField(null=True, blank=True)
    window_token = models.CharField(max_length=64, blank=True)
    warnings = models.PositiveSmallIntegerField(default=0)
    submitted_at = models.DateTimeField(null=True, blank=True)

    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    correct = models.PositiveSmallIntegerField(default=0)
    wrong = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f'{self.candidate_name} · {self.mock}'

    @property
    def is_submitted(self):
        return self.status == self.SUBMITTED

    @property
    def short_id(self):
        return self.id.hex[:8].upper()


class Response(models.Model):
    NOT_VISITED = 'not_visited'
    NOT_ANSWERED = 'not_answered'
    ANSWERED = 'answered'
    MARKED = 'marked'
    ANSWERED_MARKED = 'answered_marked'
    STATUSES = [
        (NOT_VISITED, 'Not Visited'),
        (NOT_ANSWERED, 'Not Answered'),
        (ANSWERED, 'Answered'),
        (MARKED, 'Marked for Review'),
        (ANSWERED_MARKED, 'Answered & Marked for Review'),
    ]

    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.PositiveSmallIntegerField(help_text='Question number shown to the candidate.')
    selected = models.ForeignKey(Option, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default=NOT_VISITED)
    seconds_spent = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['number']
        constraints = [
            models.UniqueConstraint(fields=['attempt', 'question'], name='unique_attempt_question'),
            models.UniqueConstraint(fields=['attempt', 'number'], name='unique_attempt_number'),
        ]

    @property
    def counts_as_answer(self):
        # As in the real exam, "Answered & Marked for Review" is evaluated.
        return self.selected_id is not None and self.status in (self.ANSWERED, self.ANSWERED_MARKED)


class ProctorEvent(models.Model):
    """Audit trail of suspicious client behaviour during an attempt."""

    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='events')
    kind = models.CharField(max_length=30)
    counted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
