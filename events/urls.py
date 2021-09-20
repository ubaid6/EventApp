from django.contrib import admin
from django.urls import path
from . import views
from . views import editEvent, deleteEvent

urlpatterns = [
    path('', views.home, name='events-home'),
    path('create/', views.create, name='create'),
    path('editevent/<int:pk>', editEvent.as_view(), name='edit'),
    path('deleteevent/<int:pk>', deleteEvent.as_view(), name='delete'),
    path('subscribe/<int:id>', views.attend, name='attend'),
    path('unsubscribe/<int:id>', views.unattend, name='unattend'),
    path('myevents/', views.myEvents, name='my-events')
]