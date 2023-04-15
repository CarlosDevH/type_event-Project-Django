from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
@login_required
def new_event(request):
    if request.method == "GET":
        return render(request, 'new_event.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        start_date = request.POST.get('start_data')
        end_date = request.POST.get('end_data')
        workload = request.POST.get('workload')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')
        
        logo = request.FILES.get('logo')

        event = Event(
            creator = request.user,
            name = name,
            description = description,
            start_date = start_date,
            end_date = end_date,
            workload = workload,
            cor_principal = cor_principal,
            cor_secundaria = cor_secundaria,
            cor_fundo = cor_fundo,
            logo = logo,
        )

        event.save()

        messages.add_message(request, constants.SUCCESS, 'Evento cadastrado com sucesso')
        return redirect(reverse('new_event'))
    
def manage_event(request):
    if request.method == "GET":
        name = request.GET.get('name')
        events = Event.objects.filter(creator = request.user)

        if name:
            events = events.filter(name__contains=name)

        return render(request, 'manage_event.html', {'events': events})

def register_event(request, id):
    event = get_object_or_404(Event, id = id)
    if request.method == 'GET':
         return render(request, 'register_event.html', {'event': event})
