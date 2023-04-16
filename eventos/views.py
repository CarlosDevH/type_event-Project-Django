from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Certificate
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants
from django.http import Http404
import csv
from secrets import token_urlsafe
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
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
    elif request.method == 'POST':
        #Validar se o participante ja faz parte do evento, para não poder se inscrever dnv
        event.participants.add(request.user)
        event.save()
        messages.add_message(request, constants.SUCCESS, 'Inscrição realizada com sucesso')

        return redirect(f'/event/register_event/{event.id}')
    
def participants_event(request, id):
    event = get_object_or_404(Event, id=id)
    if not event.creator == request.user:
        raise Http404("Esse evento não é seu")
    if request.method == "GET":
        participants = event.participants.all()
        return render(request, 'participants_event.html', {'event': event, 'participants': participants})

def create_csv(request, id):
    event = get_object_or_404(Event, id=id)
    if not event.creator == request.user:
        raise Http404('Esse evento não é seu')
    participants = event.participants.all()
    
    token = f'{token_urlsafe(6)}.csv'
    path = os.path.join(settings.MEDIA_ROOT, token)

    with open(path, 'w') as arq:
        writer = csv.writer(arq, delimiter=",")
        for participant in participants:
            x = (participant.username, participant.email)
            writer.writerow(x)

    return redirect(f'/media/{token}')

def certificates_event(request, id):
    event = get_object_or_404(Event, id = id)
    if not event.creator == request.user:
        raise Http404("Esse evento não é seu")
    if request.method == "GET":
        qtd_certificates = event.participants.all().count() - Certificate.objects.filter(event=event).count() #ajudar a validar qtd ja gerada
        return render(request, 'certificates_event.html', {'qtd_certificates': qtd_certificates, 'event': event})

def create_certificate(request, id):
    event = get_object_or_404(Event, id = id)
    if not event.creator == request.user:
        raise Http404("Esse evento não é seu")
    
    path_template = os.path.join(settings.BASE_DIR, 'templates/static/event/img/template_certificado.png')
    path_fonte = os.path.join(settings.BASE_DIR, 'templates/static/fontes/arimo.ttf')

    for participant in event.participants.all():
        #TODO: validar se o certificado ja foi gerado
        #Estudar mais como funcina pillow

        img = Image.open(path_template)
        draw = ImageDraw.Draw(img)
        font_name = ImageFont.truetype(path_fonte, 80)
        font_info = ImageFont.truetype(path_fonte, 30)

        draw.text((230, 651), f"{participant.username}", font=font_name, fill=(0,0,0))
        draw.text((761, 770), f"{event.name}", font=font_info, fill=(0,0,0))
        draw.text((816, 849), f"{event.workload} horas", font=font_info, fill=(0,0,0))

        output = BytesIO()
        img.save(output, format="PNG", quality=100)
        output.seek(0)
        final_img = InMemoryUploadedFile(output,
                                         'ImageField',
                                         f'{token_urlsafe(8)}.png',
                                         'image/jpeg',
                                         sys.getsizeof(output),
                                         None
                                         )

        created_certificate = Certificate(
            certificate=final_img,
            participants=participant,
            event=event
        )
        created_certificate.save()

    messages.add_message(request, constants.SUCCESS, 'Certificados gerados com sucesso!')
    return redirect(reverse('certificates_event', kwargs ={"id":event.id}))

def seek_certificate(request, id):
    event = get_object_or_404(Event, id = id)
    if not event.creator == request.user:
        raise Http404("Esse evento não é seu")
    
    email = request.POST.get('email')
    certificate = Certificate.objects.filter(event=event).filter(participants__email=email).first()

    if not certificate:
        messages.add_message(request, constants.ERROR, 'Esse certificado ainda não foi gerado')
        return redirect(reverse('certificates_event', kwargs = {'id':event }))
    
    return redirect(certificate.certificates.url)
