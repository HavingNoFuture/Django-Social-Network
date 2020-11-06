from django.urls import path, include

from . import views


urlpatterns = [
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        views.AccountActivationView.as_view(),
        name="account_activation",
    ),
    path("", views.DashboardView.as_view(), name="dashboard"),
]
