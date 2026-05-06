from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="http://localhost:8080", permanent=False)),
    path("admin/", admin.site.urls),
    path("api/", include("clinic.urls")),
]
