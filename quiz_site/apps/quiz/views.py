from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.list import ListView


from .forms import QuestionChoices, CreateQuizForm, AddQuestionsForm, AddChoiceForm
from .models import Quiz


class ListQuizes(ListView):
	model = Quiz


class DetialQuiz(View):
	"""Present an overview of the quiz."""

	def get(self, request, quiz_id):
		"""Handle get request."""
		quiz_object = get_object_or_404(Quiz, id=quiz_id)
		first_question_object = quiz_object.multiplechoicequestion_set.first()
		template_name = "quiz/detailquiz.html"
		context = {
			"quiz_object": quiz_object, 
			"first_question_object": first_question_object,
		}
		return render(request, template_name, context)



class PlayQuiz(View):
	"""Play a game of quiz."""
	
	def get(self, request, quiz_id, question):
		"""Handle get request."""
		
		quiz_object = get_object_or_404(Quiz, id=quiz_id)
		question_object, choices = self.get_question_choices(quiz_object, question)

		if question_object == quiz_object.multiplechoicequestion_set.first():
			request.session["score"] = 0
			request.session["incorrect"] = {}



		choices_form = QuestionChoices()
		choices_form.fields["choices"].queryset = choices

		template_name = "quiz/playquiz.html"
		context = {
			"choices_form": choices_form,
			"question_object": question_object
		}
		return render(request, template_name, context)

	def post(self, request, quiz_id, question):
		"""Handle post request."""
		quiz_object = get_object_or_404(Quiz, id=quiz_id)
		question_object, choices = self.get_question_choices(quiz_object, question)



		choices_form = QuestionChoices(request.POST)
		choices_form.fields["choices"].queryset = choices

		if choices_form.is_valid():
			user_choice = choices_form.cleaned_data["choices"]

			if user_choice.is_answer:
				request.session["score"] += 1
			else:
				correct_choice = choices.get(is_answer=True)
				incorrect_dict = request.session["incorrect"]
				incorrect_dict[question] = {
					"user_choice": user_choice.choice_name,
					"correct_choice": correct_choice.choice_name,
				}
				request.session["incorrect"] = incorrect_dict


			return self.send_next_question(quiz_object, question_object)
		else:
			print(choices_form.errors)

	@staticmethod
	def send_next_question(quiz_object, question_object):
		prev_question_id = question_object.id
		next_question_object = quiz_object.multiplechoicequestion_set.filter(id__gt=prev_question_id).first()

		if next_question_object is None:
			return redirect("end-quiz")

		question = next_question_object.question
		quiz_id = quiz_object.id

		return redirect("play-quiz", quiz_id=quiz_id, question=question)


	@staticmethod
	def get_question_choices(quiz_object, question):
		"""Return a questions and all the choices allocated to it."""
		question_object = quiz_object.multiplechoicequestion_set.get(question=question)
		choices = question_object.choice_set.all()
		return question_object, choices


class EndQuiz(View):
	"""Show results when quiz ends."""

	def get(self, request):
		"""Handle get request."""
		incorrectly_answered = request.session["incorrect"]

		template_name = "quiz/endquiz.html"
		context = {
			"score": request.session["score"],
			"incorrectly_answered": incorrectly_answered,
		}
		return render(request, template_name, context)


class CreateQuiz(LoginRequiredMixin, View):
	"""Create a quiz."""

	def get(self, request):
		"""Handle get request."""
		create_quiz_form = CreateQuizForm()

		template_name = "quiz/createquiz.html"
		context = {
			"create_quiz_form": create_quiz_form,
		}

		return render(request, template_name, context)

