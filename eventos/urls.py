from django.urls import path
from . import views

urlpatterns = [
    path('new_event/', views.new_event, name="new_event"),
    path('manage_event/', views.manage_event, name = "manage_event"),
    path('register_event/<int:id>', views.register_event, name = "register_event"),
    path('participants_event/<int:id>/', views.participants_event, name = "participants_event"),
    path('create_csv/<int:id>/', views.create_csv, name="create_csv"),
    path('certificates_event/<int:id>/', views.certificates_event, name="certificates_event"),
    path('create_certificate/<int:id>/', views.create_certificate, name="create_certificate"),
    path('seek_certificate/<int:id>/', views.seek_certificate, name="seek_certificate")
]