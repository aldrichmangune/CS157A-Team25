from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('createTextbook', views.createTextbook, name='create_listing')
]