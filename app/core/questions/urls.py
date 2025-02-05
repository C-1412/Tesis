from django.urls import path
from core.questions.views import QuestionsListView, QuestionDetailView, MarkAnswersCompleteView

app_name = 'questions'

urlpatterns = [
    path('', QuestionsListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('completadas/', MarkAnswersCompleteView.as_view(), name='completadas'),
]
