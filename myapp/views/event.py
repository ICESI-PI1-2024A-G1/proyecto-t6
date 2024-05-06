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
    """
    Registers an event based on the provided event request.

    Args:
    - request: HttpRequest object.
    - eventRequest: EventRequest object.

    Returns:
    - Redirects to the event list page.
    """
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
    """
    Displays a list of events based on search parameters.

    Args:
    - request: HttpRequest object.

    Returns:
    - Rendered template displaying the list of events.
    """
    search_term = request.GET.get('search', '')
    filter_by = request.GET.get('filter_by', 'id')
    if search_term:
        if filter_by == 'id':
            eventos = Event.objects.filter(id__icontains=search_term, estado_solicitud='En curso')
        elif filter_by == 'titulo':
            eventos = Event.objects.filter(titulo__icontains=search_term, estado_solicitud='En curso')
        elif filter_by == 'presupuesto':
            eventos = Event.objects.filter(presupuesto__icontains=search_term, estado_solicitud='En curso')
    else:
        eventos = Event.objects.filter(estado_solicitud='En curso')

    return render(request, 'eventsList.html', {'eventos': eventos})


@login_required
def saveTasks(request, evento_id):
    """
    Saves the tasks related to an event.

    Args:
    - request: HttpRequest object.
    - evento_id: ID of the event.

    Returns:
    - Redirects to the event list page.
    """
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
    """
    Marks an event as finished.

    Args:
    - request: HttpRequest object.
    - evento_id: ID of the event.

    Returns:
    - Redirects to the event list page.
    """
    evento = get_object_or_404(Event, id=evento_id)

    # Change the request status to "Finished"
    evento.estado_solicitud = 'Finalizado'
    evento.save()
    message = f"Se ha finalizado el evento."
    messages.success(request, message)

    # Send notification when an event is finished
    message_notification = "Se ha finalizado un evento. Puedes ver los detalles en el historial de eventos"
    notificacion = Notification.objects.create(
        message=message_notification, url='/event-registry')

    # Get the user's email associated with the event
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
    """
    Displays a list of finished events.

    Args:
    - request: HttpRequest object.

    Returns:
    - Rendered template displaying the list of finished events.
    """
    user = request.user
    search_term = request.GET.get('search', '')
    filter_by = request.GET.get('filter_by', 'id')
    if search_term:
        if filter_by == 'id':
            events = Event.objects.filter(id__icontains=search_term, estado_solicitud='Finalizado')
        elif filter_by == 'titulo':
            events = Event.objects.filter(titulo__icontains=search_term, estado_solicitud='Finalizado')
        elif filter_by == 'presupuesto':
            events = Event.objects.filter(presupuesto__icontains=search_term, estado_solicitud='Finalizado')
    else:
        events = Event.objects.filter(estado_solicitud='Finalizado')

    return render(request, 'finishedEvents.html', {'eventos': events})


@login_required
def reset_ceremony(request):
    """
    Resets the ceremony by deleting all ceremony activities and resetting ceremony dates.

    Args:
    - request: HttpRequest object.

    Returns:
    - Redirects to the ceremony planning page.
    """
    if request.method == 'POST':
        # Delete all ceremony activities
        CeremonyActivity.objects.all().delete()

        # Reset or create a new ceremony
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
    """
    Displays the ceremony planning page and handles adding activities to the ceremony.

    Args:
    - request: HttpRequest object.

    Returns:
    - Rendered template displaying the ceremony planning page.
    """
    # Check if an active ceremony exists
    ceremony = Ceremony.objects.first()

    # If no ceremony exists, create one automatically
    if not ceremony:
        reset_ceremony(request)
        ceremony_activities = CeremonyActivity.objects.all
        form = CeremonyActivityForm(request.POST)

    # Get ceremony activities
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
    """
    Marks a ceremony activity as completed.

    Args:
    - request: HttpRequest object.
    - activity_id: ID of the activity.

    Returns:
    - Redirects to the ceremony planning page.
    """
    if request.method == 'POST':

        activity = CeremonyActivity.objects.get(id=activity_id)
        activity.completed = True
        activity.save()

    return redirect('ceremony-plan')


@login_required
def guardar_evento(request):
    """
    Saves the status of an event (e.g., food, transport, extras).

    Args:
    - request: HttpRequest object.

    Returns:
    - Redirects to the appropriate event list page.
    """
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
        print(estado_extras)


    # Redirect to the desired page after saving
    if (request.user.groups.values_list("id", flat=True).first() == 2):
        return redirect('event-list-apoyo')

    return redirect('event-list')


@login_required
def eventListApoyo(request):
    """
    Displays a list of events for support staff.

    Args:
    - request: HttpRequest object.

    Returns:
    - Rendered template displaying the list of events for support staff.
    """
    eventos = Event.objects.filter(estado_solicitud='En curso')
    return render(request, 'eventsListApoyo.html', {'eventos': eventos})


@login_required
def finishEventApoyo(request):
    """
    Displays a list of finished events for support staff.

    Args:
    - request: HttpRequest object.

    Returns:
    - Rendered template displaying the list of finished events for support staff.
    """
    events = Event.objects.filter(estado_solicitud='Finalizado')
    return render(request, 'finishedEventsApoyo.html', {'eventos': events})
