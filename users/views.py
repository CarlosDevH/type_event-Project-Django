from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        user_name = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not password == confirm_password:
            return redirect('/users/register')

        #Validar força da senha 
        user = User.objects.filter(username = user_name)
        
        if user.exists():
            return redirect('/users/register')
        
        user = User.objects.create_user(username = user_name, email  = email, password = password)
        user.save()
        return HttpResponse("Usuário Adicionado")
    
