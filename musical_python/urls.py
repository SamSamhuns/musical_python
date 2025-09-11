from django.urls import re_path
from django.contrib import admin
from musical_python import views

urlpatterns = [
    re_path(r"^submit", views.submit),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^$", views.home, name="home"),
    re_path(r"^instruments", views.instruments, name="instruments"),
    re_path(r"^references", views.references, name="references"),
]
