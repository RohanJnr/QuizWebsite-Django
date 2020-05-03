from django.shortcuts import render
from django.views import View


class HomeView(View):
	"""Landing page of the website."""

	def get(self, request):
		"""Render home page."""
		template_name = "home/index.html"
		context={}
		return render(request, template_name, context)
