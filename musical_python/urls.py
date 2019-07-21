from django.conf.urls import url
from django.contrib import admin
from musical_python import views

urlpatterns = [
  url(r'^submit', views.submit),
  url(r'^admin/', admin.site.urls),
  url(r'^$', views.home, name='home'),
  url(r'^instruments', views.instruments, name='instruments'),
  url(r'^references', views.references, name='references'),
]
