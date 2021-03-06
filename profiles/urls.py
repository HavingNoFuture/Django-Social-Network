from django.urls import path

from profiles import views


app_name = "profiles"

urlpatterns = [
    path("edit/", views.ProfileEditView.as_view(), name="edit"),
    path("me/", views.MyProfileView.as_view(), name="me"),
    path("<str:slug>/", views.ProfileView.as_view(), name="detail"),
]
