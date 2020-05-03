from django.urls import path

from .views import RegisterView, LoginView, LogoutView


urlpatterns = [
	path("accounts/register/", RegisterView.as_view(), name="register"),
	path("accounts/login/", LoginView.as_view(), name="login"),
	path("accounts/logout/", LogoutView.as_view(), name="logout"),
]