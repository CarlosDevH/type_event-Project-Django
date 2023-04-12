from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.urls import reverse
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
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect(reverse('register'))

        #Validar força da senha 
        user = User.objects.filter(username = user_name)
        
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário cadastrado com esse email')
            return redirect(reverse('register'))
        
        user = User.objects.create_user(username = user_name, email = email, password = password)
        user.save()
        messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso!')

        return redirect(reverse('login'))
    
