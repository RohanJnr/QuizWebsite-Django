from django import forms

from .models import Quiz, MultipleChoiceQuestion, Choice


class QuestionChoices(forms.Form):
	choices = forms.ModelChoiceField(
		queryset=MultipleChoiceQuestion.objects.none(),
	)


class CreateQuizForm(forms.ModelForm):
	class Meta:
		model = Quiz
		fields = ["title", "description"]


class AddQuestionsForm(forms.ModelForm):
	class Meta:
		model = MultipleChoiceQuestion
		fields = ["question"]


class AddChoiceForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ["choice_name", "is_answer"]
