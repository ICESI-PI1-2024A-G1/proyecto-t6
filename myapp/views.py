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
                'error': 'Nombre de usuario o constraseña incorrecta!'
            })
        else:
            login(request, user)
            return redirect('index')


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
                'error': 'Nombre de usuario o constraseña incorrecta!'
            })
        else:
            login(request, user)
            return redirect('index')


def signout(request):
    logout(request)
    return redirect('academicUsersLogin')


@login_required
def createEventRequest(request):
    if request.method == 'POST':
        form = EventRequestForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user  # Asigna el usuario a la solicitud
            solicitud.save()
            messages.success(
                request, 'La solicitud de evento se ha creado correctamente.')
            # Redirige a la misma página para mostrar el formulario limpio
            return redirect('create-event-request')
    else:
        form = EventRequestForm()
    return render(request, 'createEventRequest.html', {'form': form})

def eventRecord(request):
    eventos = EventRequest.objects.all()
    return render(request, 'event_record.html', {'eventos': eventos})

def lista_eventos(request):
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
            return redirect('lista_eventos')
    else:
        form = EstadoSolicitudForm()
    return render(request, 'lista_eventos.html', {'eventos': eventos, 'form': form})
