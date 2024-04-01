from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import EventRequestForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import EventRequest, Event
from .forms import EstadoSolicitudForm
from django.db.models import Q

# Create your views here.


def home(request):
    return render(request, "home.html")




def index(request):
    group = request.user.groups.values_list("id", flat=True).first()
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    if group == 1:
        return render(request, "index1.html", {'username': username})
    if group == 2:
        return render(request, "index2.html", {'username': username})
    return render(request, "index3.html", {'username': username})



def academicMembersLogin(request):
    if request.method == "GET":
        return render(
            request, "loginAcademicCommunity.html", {"form": AuthenticationForm}
        )
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "loginAcademicCommunity.html",
                {
                    "form": AuthenticationForm,
                    "error": "Nombre de usuario o contraseña incorrecta!",
                },
            )
        else:
            group = user.groups.values_list('id', flat=True).first()
            print("ID del usuario:", group)
            if (group==3 or group==4):
                login(request, user)
                return redirect("index")

            return render(
                request,
                "loginAcademicCommunity.html",
                {
                    "form": AuthenticationForm,
                    "error": "Las credenciales no son de un mienbro la comunidad!",
                },
            )


def ccsaLogin(request):
    if request.method == "GET":
        return render(request, "CCSAlogin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "CCSAlogin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Nombre de usuario o contraseña incorrecta!",
                },
            )
        else:
            group = user.groups.values_list("id", flat=True).first()
            if group == 1 or group == 2:
                login(request, user)
                return redirect("index")

            return render(
                request,
                "CCSAlogin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Las credenciales no son de un miembro de la CCSA!",
                },
            )


def signout(request):
    logout(request)
    return redirect("home")


@login_required
def createEventRequest(request):
    if request.method == "POST":
        form = EventRequestForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.usuario = request.user  # Asigna el usuario a la solicitud
            solicitud.save()

            # Mostrar notificacion de eventos creados con detalles

            message = f"Se ha creado una solicitud de evento: {solicitud}"
            messages.success(request, message)
            return redirect("create-event-request")
    else:
        form = EventRequestForm()
    return render(request, "createEventRequest.html", {"form": form})


def eventRequestRecord(request):
    user = request.user
    group = user.groups.values_list('id', flat=True).first()

    if group in [3, 4]:
        events = EventRequest.objects.filter(usuario_id=user)
        return render(request, 'eventRequestRecord_2.html', {'eventos': events})
    else:
        events = EventRequest.objects.filter(Q(estado_solicitud='aprobada') | Q(estado_solicitud='rechazada'))
        return render(request, 'eventRequestRecord.html', {'eventos': events})

#Ver solicitudes de eventos, cambiar estado de eventos
#Mostrar notificacion de eventos creados con detalles

# Como no hay un campo que diferencie al usuario de CCSlogin y el AcademyUser
# en los modelos que tienen para almacenar esos usuarios, cualquiera de
# los dos que este logueado puede acceder a la seccion de aprobar/rechazar eventos.
# Cuando se arregle el problema se realizará la respectiva actualizacion
@login_required
def eventRequestList(request):
    eventos = EventRequest.objects.all()
    if request.method == "POST":
        form = EstadoSolicitudForm(request.POST)
        print(request.POST)
        if form.is_valid():
            evento_id = form.cleaned_data["evento_id"]
            estado_solicitud = form.cleaned_data["estado_solicitud"]
            evento = EventRequest.objects.get(id=evento_id)
            evento.estado_solicitud = estado_solicitud
            evento.save()
            if estado_solicitud == "aprobada":
                eventRegistration(request, evento)
                message = f"Se ha aceptado la solicitud de evento. Puede encontrarla en la lista de eventos."
                messages.success(request, message)
            return redirect("/event-requests")
    else:
        form = EstadoSolicitudForm()
    return render(
        request,
        "eventsRequestList.html",
        {"eventos": eventos, "form": form, "messages": messages.get_messages(request)},
    )


@login_required
def eventList(request):
    eventos = EventRequest.objects.filter(estado_solicitud = 'aprobada')
    return render(request, 'eventsList.html', {'eventos': eventos})

@login_required
def saveTasks(request, evento_id):
    if request.method == 'POST':
        event = EventRequest.objects.get(pk=evento_id)
        event.lugar = request.POST.get('lugar')
        event.presupuesto = request.POST.get('presupuesto')
        event.alimentacion = request.POST.get('alimentacion')
        event.transporte = request.POST.get('transporte')
        event.extra = request.POST.get('extra')
        event.save()
        return redirect('event-list')
    return redirect('event-list')


@login_required
def eventList(request):
    eventos = EventRequest.objects.filter(estado_solicitud = 'aprobada')
    return render(request, 'eventsList.html', {'eventos': eventos})

@login_required
def saveTasks(request, evento_id):
    if request.method == 'POST':
        event = EventRequest.objects.get(pk=evento_id)
        event.lugar = request.POST.get('lugar')
        event.presupuesto = request.POST.get('presupuesto')
        event.alimentacion = request.POST.get('alimentacion')
        event.transporte = request.POST.get('transporte')
        event.extra = request.POST.get('extra')
        event.save()
        return redirect('event-list')
    return redirect('event-list')


@login_required
def eventRegistration(request, eventRequest):
    event = Event(request.POST)
    event.id = eventRequest.id
    event.usuario = eventRequest.usuario
    event.lugar = eventRequest.lugar
    event.fecha_inicio = eventRequest.fecha_inicio
    event.fecha_fin = eventRequest.fecha_fin
    event.presupuesto = eventRequest.presupuesto
    event.alimentacion = eventRequest.alimentacion
    event.transporte = eventRequest.transporte
    event.profesor = eventRequest.profesor
    event.save()
    print("Se creo el nuevo evento")
