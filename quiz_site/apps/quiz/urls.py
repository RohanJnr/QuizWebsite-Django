from django.urls import path

from .views import PlayQuiz, DetialQuiz, EndQuiz, ListQuizes

urlpatterns = [
	path("quiz/<int:quiz_id>", DetialQuiz.as_view(), name="detail-quiz"),
	path("quiz/<int:quiz_id>/<str:question>", PlayQuiz.as_view(), name="play-quiz"),
	path("quiz/end", EndQuiz.as_view(), name="end-quiz"),
	path('quiz/list', ListQuizes.as_view(), name='list-quizes'),
]
