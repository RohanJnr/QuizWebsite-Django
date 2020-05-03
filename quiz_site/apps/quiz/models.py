from django.db import models

from quiz_site.apps.users.models import Account


class Quiz(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField()
	author = models.ForeignKey(Account, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = ("Quiz")
		verbose_name_plural = ("Quizes")


class MultipleChoiceQuestion(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = models.TextField()

	def __str__(self):
		return f"{self.quiz} - {self.question}"

	class Meta:
		verbose_name = ("MCQ")
		verbose_name_plural = ("MCQs")

class Choice(models.Model):
	question = models.ForeignKey(MultipleChoiceQuestion, on_delete=models.CASCADE)
	choice_name = models.CharField(max_length=200)

	def __str__(self):
		return f"{self.question} - {self.choice}" 

	class Meta:
		verbose_name = ("Choice")
		verbose_name_plural = ("Choices")
