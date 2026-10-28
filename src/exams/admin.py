from django.contrib import admin

from .models import (
    Attempt, Exam, ExamCategory, MockTest, Option, Passage, Plan, ProctorEvent, Question, Section,
)


class ExamInline(admin.TabularInline):
    model = Exam
    extra = 0
    prepopulated_fields = {'slug': ('short_name',)}


@admin.register(ExamCategory)
class ExamCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ExamInline]


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0


@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'exam', 'stage', 'is_free', 'is_published', 'order']
    list_filter = ['exam', 'is_free', 'is_published']
    list_editable = ['is_free', 'is_published', 'order']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SectionInline]


class OptionInline(admin.TabularInline):
    model = Option
    extra = 5
    max_num = 5


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'topic', 'section']
    list_filter = ['section__mock', 'section__name', 'topic']
    search_fields = ['text']
    autocomplete_fields = ['passage']
    inlines = [OptionInline]


@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'section', 'layout']
    list_filter = ['section__mock']
    search_fields = ['directions', 'body']


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'exam', 'price_inr', 'is_active']


class ProctorEventInline(admin.TabularInline):
    model = ProctorEvent
    extra = 0
    can_delete = False
    readonly_fields = ['kind', 'counted', 'created_at', 'ip']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['candidate_name', 'mock', 'status', 'score', 'warnings', 'started_at']
    list_filter = ['status', 'submit_reason', 'mock']
    readonly_fields = [f.name for f in Attempt._meta.fields]
    inlines = [ProctorEventInline]

    def has_add_permission(self, request):
        return False
