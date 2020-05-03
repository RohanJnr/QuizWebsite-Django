from django.contrib import admin

from .models import Quiz, MultipleChoiceQuestion, Choice

admin.site.register(Quiz)
admin.site.register(MultipleChoiceQuestion)
admin.site.register(Choice)
