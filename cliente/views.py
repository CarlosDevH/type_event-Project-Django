from django.shortcuts import render
from eventos.models import Certificate
# Create your views here.
def my_certificates(request):
    certificates = Certificate.objects.filter(participants = request.user)
    return render(request, 'my_certificates.html', {'certificates':certificates})