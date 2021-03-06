from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="dashboard", permanent=False), name="main"),
    path("profiles/", include("profiles.urls", namespace="profiles")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("social-auth/", include("social_django.urls", namespace="social")),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
