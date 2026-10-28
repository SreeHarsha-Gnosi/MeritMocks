from django.urls import path

from . import views

urlpatterns = [
    path('exams/<slug:slug>/', views.exam_detail, name='exam_detail'),
    path('mock/<slug:slug>/', views.instructions, name='instructions'),
    path('attempt/<uuid:attempt_id>/', views.attempt_page, name='attempt'),
    path('attempt/<uuid:attempt_id>/result/', views.result, name='result'),
    path('attempt/<uuid:attempt_id>/solutions/', views.solutions, name='solutions'),
    path('attempt/<uuid:attempt_id>/api/state', views.api_state, name='api_state'),
    path('attempt/<uuid:attempt_id>/api/question', views.api_question, name='api_question'),
    path('attempt/<uuid:attempt_id>/api/answer', views.api_answer, name='api_answer'),
    path('attempt/<uuid:attempt_id>/api/event', views.api_event, name='api_event'),
    path('attempt/<uuid:attempt_id>/api/summary', views.api_summary, name='api_summary'),
    path('attempt/<uuid:attempt_id>/api/submit', views.api_submit, name='api_submit'),
]
