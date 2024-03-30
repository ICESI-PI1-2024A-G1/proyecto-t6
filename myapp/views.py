from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import EventRequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import EventRequest
from .forms import EstadoSolicitudForm
# Create your views here.

def home(request):
    return render(request, 'home.html')

def index(request):
    return render(request, 'index.html')


def academicMembersLogin(request):
    if request.method == 'GET':
        return render(request, 'loginAcademicCommunity.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'loginAcademicCommunity.html', {
                'form': AuthenticationForm,
                'error': 'Nombre de usuario o contraseña incorrecta!'
            })
        else:
            group = user.groups.values_list('name', flat=True).first()
            if (group==3 or group==4):
                login(request, user)
                return redirect('index')
            
            return render(request, 'loginAcademicCommunity.html', {
                'form': AuthenticationForm,
                'error': 'Las credenciales no son de un mienbro la comunidad!'
            })


def ccsaLogin(request):
    if request.method == 'GET':
        return render(request, 'CCSAlogin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )
        if user is None:
            return render(request, 'CCSAlogin.html', {
                'form': AuthenticationForm,
                'error': 'Nombre de usuario o contraseña incorrecta!'
            })
        else:
            group = user.groups.values_list('id', flat=True).first()
            print(group)
            if (group==1 or group==2):
                login(request, user)
                return redirect('index')
            
            return render(request, 'CCSAlogin.html', {
                'form': AuthenticationForm,
                'error': 'Las credenciales no son de un miembro de la CCSA!'
            })


def signout(request):
    logout(request)
    return redirect('home')


@login_required
def createEventRequest(request):
    if request.method == 'POST':
        form = EventRequestForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user  # Asigna el usuario a la solicitud
            solicitud.save()

            #Mostrar notificacion de eventos creados con detalles

            message = f'Se ha creado una solicitud de evento: {solicitud}'
            messages.success(request, message)
            return redirect('create-event-request')
    else:
        form = EventRequestForm()
    return render(request, 'createEventRequest.html', {'form': form})

def eventRecord(request):
    user = request.user.id
    events = EventRequest.objects.filter(usuario_id = user)
    return render(request, 'eventRecord.html', {'eventos': events})


#Ver solicitudes de eventos, cambiar estado de eventos
#Mostrar notificacion de eventos creados con detalles

#Como no hay un campo que diferencie al usuario de CCSlogin y el AcademyUser
# en los modelos que tienen para almacenar esos usuarios, cualquiera de
# los dos que este logueado puede acceder a la seccion de aprobar/rechazar eventos.
# Cuando se arregle el problema se realizará la respectiva actualizacion
@login_required
def eventsList(request):
    eventos = EventRequest.objects.all()
    if request.method == 'POST':
        form = EstadoSolicitudForm(request.POST)
        print(request.POST)
        if form.is_valid():
            evento_id = form.cleaned_data['evento_id']
            estado_solicitud = form.cleaned_data['estado_solicitud']

            evento = EventRequest.objects.get(id=evento_id)
            evento.estado_solicitud = estado_solicitud
            evento.save()
            return redirect('events-list')
    else:
        form = EstadoSolicitudForm()
    return render(request, 'eventsList.html', {'eventos': eventos, 'form': form, 'messages': messages.get_messages(request)})
