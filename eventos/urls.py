from django.urls import path
from . import views

urlpatterns = [
    path('new_event/', views.new_event, name="new_event"),
]