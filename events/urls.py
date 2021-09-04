from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='events-home'),
    path('create/', views.create, name='create'),

]