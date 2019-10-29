from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),

    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
