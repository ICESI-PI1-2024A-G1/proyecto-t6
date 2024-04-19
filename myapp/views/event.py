from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from myapp.models import EventRequest
from myapp.models import Event

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

@login_required
def eventList(request):
    eventos = EventRequest.objects.filter(estado_solicitud = 'Aprobada')
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
def finishEvent(request, evento_id):
    evento = get_object_or_404(EventRequest, id=evento_id)

    # Cambiar el estado de solicitud a "Finalizado"
    evento.estado_solicitud = 'Finalizado'
    evento.save()
    message = f"Se ha finalizado el evento."
    messages.success(request, message)

    return redirect('event-list') 

@login_required
def eventRegistry(request):
    user = request.user
    events = EventRequest.objects.filter(estado_solicitud='Finalizado')
    return render(request, 'finishedEvents.html', {'eventos': events})