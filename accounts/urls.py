from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "activate/<str:uidb64>/<str:token>/",
        views.AccountActivationView.as_view(),
        name="account_activation",
    ),
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("edit/", views.AccountEditView.as_view(), name="edit"),
]
