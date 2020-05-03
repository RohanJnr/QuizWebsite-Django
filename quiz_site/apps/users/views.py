from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from .forms import UserCreationForm, UserLoginForm
from .mixins import RestrictPagesIfLoggedMixin


class RegisterView(RestrictPagesIfLoggedMixin, View):
	"""Handle user authentication."""

	def get(self, request):
		template_name = "users/register.html"
		context = {
			"register_form": UserCreationForm
		}
		return render(request, template_name, context)

	def post(self, request):
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("home")
		else:
			print(form.errors)
			return redirect("register")


class LoginView(RestrictPagesIfLoggedMixin, View):
	"""Handle user authentication and login."""
	def get(self, request):
		"""Handle get request."""
		login_form = UserLoginForm()
		template_name = "users/login.html"
		context={
			"login_form": login_form
		}
		return render(request, template_name, context)

	def post(self, request):
		login_form = UserLoginForm(request.POST)
		email = request.POST["email"]
		password = request.POST["password"]
		user = authenticate(request, email=email, password=password)
		# validation is done in forms.py
		login(request, user)
		return redirect("home")


class LogoutView(LoginRequiredMixin, View):
	"""Logout a user."""

	def get(self, request):
		logout(request)
		return redirect("home")

