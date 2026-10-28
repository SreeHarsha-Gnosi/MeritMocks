from django.shortcuts import render

from exams.models import ExamCategory, MockTest, Plan


def home(request):
    featured = (
        MockTest.objects.filter(is_published=True, is_free=True)
        .select_related('exam')
        .prefetch_related('sections')
        .first()
    )
    pro_mocks = []
    plan = None
    if featured:
        pro_mocks = MockTest.objects.filter(exam=featured.exam, is_published=True, is_free=False)
        plan = Plan.objects.filter(exam=featured.exam, is_active=True).first()
    return render(request, 'core/home.html', {
        'categories': ExamCategory.objects.prefetch_related('exams'),
        'featured': featured,
        'pro_mocks': pro_mocks,
        'plan': plan,
    })
