from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from myapp.forms import EventRequestForm
from myapp.models import EventRequest
from myapp.forms import EstadoSolicitudForm
from django.db.models import Q
from .event import eventRegistration


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

@login_required
def eventRequestRecord(request):
    user = request.user
    group = user.groups.values_list('id', flat=True).first()

    if group in [3, 4]:
        events = EventRequest.objects.filter(usuario_id=user)
        return render(request, 'eventRequestRecord_2.html', {'eventos': events})
    else:
        events = EventRequest.objects.filter(Q(estado_solicitud='aprobada') | Q(estado_solicitud='rechazada'))
        return render(request, 'eventRequestRecord.html', {'eventos': events})
    
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
    
