from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from myapp.models import EventRequest
from myapp.models import Event, Ceremony, CeremonyActivity
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from myapp.forms import CeremonyActivityForm


from myapp.models import Notification


@login_required
def eventRegistration(request, eventRequest):
    event = Event(request.POST)
    event.id = eventRequest.id
    event.usuario = eventRequest.usuario
    event.titulo = eventRequest.titulo
    event.descripcion = eventRequest.descripcion
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
    eventos = Event.objects.filter(estado_solicitud='En curso')
    return render(request, 'eventsList.html', {'eventos': eventos})


@login_required
def saveTasks(request, evento_id):
    if request.method == 'POST':
        event = Event.objects.get(pk=evento_id)
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
    evento = get_object_or_404(Event, id=evento_id)

    # Cambiar el estado de solicitud a "Finalizado"
    evento.estado_solicitud = 'Finalizado'
    evento.save()
    message = f"Se ha finalizado el evento."
    messages.success(request, message)

    # Enviar notificacion cuando se finalice un evento
    message_notification = "Se ha finalizado un evento. Puedes ver los detalles en el historial de eventos"
    notificacion = Notification.objects.create(
        message=message_notification, url='/event-registry')

    # Obtener el correo electrónico del usuario asociado al evento
    user_email = evento.usuario.email
    asunto = "Encuesta de Satisfacción: ¡Queremos escucharte!"
    url_form = "https://forms.gle/y1LujHetTb7Qq6zv7"

    cuerpo = "Hola, Esperamos que haya tenido una experiencia satisfactoria con nuestro servicio. Para seguir mejorando y ofrecerle un servicio excepcional, le invitamos a completar nuestra Encuesta de Satisfacción. Por favor, tómese unos minutos para responder a las siguientes preguntas. Su opinión es muy valiosa para nosotros: "
    email = EmailMessage(asunto, cuerpo + url_form,
                         "freyaicesi@gmail.com", [user_email])
    email.send()
    print("Se ha enviado un email a: " + user_email)

    return redirect('event-list')


@login_required
def eventRegistry(request):
    user = request.user
    events = Event.objects.filter(estado_solicitud='Finalizado')
    return render(request, 'finishedEvents.html', {'eventos': events})


@login_required
def reset_ceremony(request):
    if request.method == 'POST':
        # Eliminar todas las actividades de la ceremonia
        CeremonyActivity.objects.all().delete()

        # Reiniciar la ceremonia si existe o crear una nueva
        ceremony, created = Ceremony.objects.get_or_create(
            title="Ceremonia de grado",
            defaults={
                'start_date': "2024-01-01",
                'end_date': "2024-01-01",
            }
        )

        ceremony.start_date = "2024-01-01"
        ceremony.end_date = "2024-01-01"
        ceremony.save()

        messages.success(request, 'Ceremony reset successfully.')
        return redirect('ceremony-plan')

    return redirect('ceremony-plan')


@login_required
def ceremonyPlan(request):
    # Verificar si existe una ceremonia activa
    ceremony = Ceremony.objects.first()

    # Si no hay ninguna ceremonia, crear una automáticamente
    if not ceremony:
        reset_ceremony(request)
        ceremony_activities = CeremonyActivity.objects.all
        form = CeremonyActivityForm(request.POST)

    # Obtener las actividades de la ceremonia
    else:
        ceremony_activities = CeremonyActivity.objects.all
        if request.method == 'POST':

            if "fecha_inicio" in request.POST and "fecha_fin" in request.POST:
                start_date = request.POST["fecha_inicio"]
                end_date = request.POST["fecha_fin"]
                ceremony.start_date = start_date
                ceremony.end_date = end_date
                ceremony.save()

                return redirect("ceremony-plan")
            else:
                form = CeremonyActivityForm(request.POST)
                if form.is_valid():
                    activity = form.save(commit=False)
                    activity.ceremony = ceremony
                    activity.save()
                    return redirect('ceremony-plan')
        else:
            form = CeremonyActivityForm()

    return render(request, 'ceremonyPlanning.html', {'ceremony': ceremony, 'ceremony_activities': ceremony_activities, 'form': form})


@login_required
def finish_activity(request, activity_id):
    if request.method == 'POST':

        activity = CeremonyActivity.objects.get(id=activity_id)
        activity.completed = True
        activity.save()

    return redirect('ceremony-plan')


@login_required
def guardar_evento(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        estado_alimentacion = request.POST.get("estado_alimentacion") == 'on'
        estado_transporte = request.POST.get('estado_transporte') == 'on'
        estado_extras = request.POST.get('estado_extras') == 'on'

        event = Event.objects.get(pk=event_id)
        event.estado_alimentacion = estado_alimentacion
        event.estado_transporte = estado_transporte
        event.estado_extras = estado_extras
        event.save()

    # Redirige a la página que desees después de guardar
    if (request.user.groups.values_list("id", flat=True).first() == 2):
        return redirect('event-list-apoyo')

    return redirect('event-list')


@login_required
def eventListApoyo(request):
    eventos = Event.objects.filter(estado_solicitud='En curso')
    return render(request, 'eventsListApoyo.html', {'eventos': eventos})


@login_required
def finishEventApoyo(request):
    events = Event.objects.filter(estado_solicitud='Finalizado')
    return render(request, 'finishedEventsApoyo.html', {'eventos': events})
