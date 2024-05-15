from datetime import date
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, Group
from myapp.models import EventRequest, Notification, Event
from myapp.views import eventRequestList, eventRegistration
from datetime import datetime
from myapp.models import Ceremony, CeremonyActivity
from django.contrib.messages import get_messages


class CreateEventRequestTestCase(TestCase):
    """
Test cases for creating an event request.
"""
    def setUp(self):
        """
        Setup method to create a test user and authenticate them, also creates a test group.
        """
        # Creamos un usuario de prueba y lo autenticamos
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Creamos un grupo
        self.group = Group.objects.create(name='Test Group')
        self.user.groups.add(self.group)

    def test_access(self):
        """
        Test access to the view for an authenticated user.
        """
        # Verificar el acceso a la vista para un usuario autenticado
        response = self.client.get(reverse('create-event-request'))
        self.assertEqual(response.status_code, 200)

    def test_form_display(self):
        """
       Test whether the form is displayed correctly.
       """
        # Verificar que el formulario se muestre correctamente
        response = self.client.get(reverse('create-event-request'))
        self.assertContains(response, '<form', count=1)

    def test_form_submission(self):
        """
       Test submission of the form.
       """
        # Verificar que el formulario se envíe correctamente
        data = {
            'titulo': 'Test Event',
            'descripcion': 'Description of Test Event',
            'lugar': 'Test Location',
            'fecha_inicio': '2024-05-20',
            'fecha_fin': '2024-05-21',
            'presupuesto': 1000,
            'alimentacion': 'Test Food',
            'transporte': 'Test Transport',
        }
        response = self.client.post(reverse('create-event-request'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de enviar el formulario

        # Verificar que el evento se haya guardado en la base de datos
        event_requests = EventRequest.objects.filter(usuario=self.user)
        self.assertEqual(event_requests.count(), 1)
        self.assertEqual(event_requests.first().titulo, 'Test Event')

    def test_hidden_professor_field(self):
        """
       Test whether the professor field is hidden for certain groups.
       """
        # Verificar que el campo de profesor esté oculto para ciertos grupos
        response = self.client.get(reverse('create-event-request'))
        self.assertNotContains(response, 'id_profesor')

class EventRequestRecordTestCase(TestCase):
    """
    Test cases for viewing event request records.
    """
    def setUp(self):
        """
        Setup method to create a test user and authenticate them, also creates a test group.
        """

        # Creamos un usuario de prueba y lo autenticamos
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        # Creamos un grupo
        self.group = Group.objects.create(name='Test Group')
        self.user.groups.add(self.group)


    def test_access(self):
        """
       Test access to the view for an authenticated user.
       """
        # Verificar el acceso a la vista para un usuario autenticado
        response = self.client.get(reverse('event-request-record'))
        self.assertEqual(response.status_code, 200)

    def test_filtering_for_different_groups(self):
        """
       Test filtering of event requests for different groups.
       """
        # Verificar que los diferentes grupos obtienen resultados filtrados apropiadamente
        # Creamos algunas solicitudes de evento para diferentes estados
        EventRequest.objects.create(
            usuario=self.user,
            titulo='Test Event 1',
            fecha_inicio=date.today(),
            fecha_fin=date.today(),
            presupuesto=100,  # Proporciona un valor válido para presupuesto
            estado_solicitud='Pendiente'
        )
        EventRequest.objects.create(
            usuario=self.user,
            titulo='Test Event 2',
            fecha_inicio=date.today(),
            fecha_fin=date.today(),
            presupuesto=200,  # Proporciona un valor válido para presupuesto
            estado_solicitud='Aprobada'
        )
        EventRequest.objects.create(
            usuario=self.user,
            titulo='Test Event 3',
            fecha_inicio=date.today(),
            fecha_fin=date.today(),
            presupuesto=300,  # Proporciona un valor válido para presupuesto
            estado_solicitud='Rechazada'
        )

        # Probamos el acceso para el grupo 3 o 4
        response = self.client.get(reverse('event-request-record'))
        self.assertContains(response, 'Test Event 2')
        self.assertContains(response, 'Test Event 3')
        self.assertNotContains(response, 'Test Event 1')

    def test_filter_by_title(self):
        """
        Test searching event requests by title.
        """
        # Verificar que la búsqueda por título funcione correctamente
        response = self.client.get(reverse('event-request-record'), {'search': 'Evento 1', 'filter_by': 'titulo'})

        self.assertNotContains(response, 'Evento 2')

class EventRequestListTestCase(TestCase):
    """
    Test cases for listing event requests.
    """
    def setUp(self):
        """
       Setup method to create a test user and some test event requests.
       """
        # Creamos un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='password')

        # Creamos algunas solicitudes de eventos de prueba
        self.event_request_1 = EventRequest.objects.create(
            usuario=self.user,
            titulo='Evento 1',
            descripcion='Descripción del evento 1',
            lugar='Lugar 1',
            fecha_inicio='2024-01-01',
            fecha_fin='2024-01-02',
            presupuesto=100.00,
            alimentacion='Comida 1',
            transporte='Transporte 1',
            estado_solicitud='Pendiente'
        )
        self.event_request_2 = EventRequest.objects.create(
            usuario=self.user,
            titulo='Evento 2',
            descripcion='Descripción del evento 2',
            lugar='Lugar 2',
            fecha_inicio='2024-01-03',
            fecha_fin='2024-01-04',
            presupuesto=200.00,
            alimentacion='Comida 2',
            transporte='Transporte 2',
            estado_solicitud='Pendiente'
        )

        # Creamos un grupo de prueba
        self.group = Group.objects.create(name='Test Group')
        self.user.groups.add(self.group)

        # Creamos un objeto RequestFactory
        self.factory = RequestFactory()

    def test_event_request_list_view(self):
        """
        Test the event request list view.
        """
        # Creamos una solicitud GET para la vista
        request = self.factory.get(reverse('event-request-list'))

        # Autenticamos al usuario en la solicitud
        request.user = self.user

        # Probamos la vista
        response = eventRequestList(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Evento 1')
        self.assertContains(response, 'Evento 2')

    def test_event_request_list_filtering(self):
        """
        Test filtering event requests by title.
        """
        # Creamos una solicitud GET para la vista con parámetros de búsqueda
        request = self.factory.get(reverse('event-request-list'), {'filter_by': 'titulo', 'search': 'Evento 1'})

        # Autenticamos al usuario en la solicitud
        request.user = self.user

        # Probamos la vista
        response = eventRequestList(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Evento 1')
        self.assertNotContains(response, 'Evento 2')


    def test_reject_event_request(self):
        """
        Test rejecting an event request.
        """
        # Creamos una solicitud POST para rechazar la solicitud de evento
        request = self.factory.post(reverse('event-request-list'), {'evento_id': self.event_request_2.id, 'estado_solicitud': 'Rechazada'})

        # Autenticamos al usuario en la solicitud
        request.user = self.user

        # Probamos la vista
        response = eventRequestList(request)
        self.assertEqual(response.status_code, 302)  # Redirección después del rechazo
        self.event_request_2.refresh_from_db()
        self.assertEqual(self.event_request_2.estado_solicitud, 'Rechazada')


class CreateEventRequestTestCase(TestCase):
    """
Test cases for creating event requests.
"""
    def setUp(self):
        """
        Setup method to create a test user, authenticate them, and create a test group.
        """
        # Creamos un usuario de prueba y lo autenticamos
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Creamos un grupo
        self.group = Group.objects.create(name='Test Group')
        self.user.groups.add(self.group)
        # Creamos un objeto RequestFactory
        self.factory = RequestFactory()

    def test_access(self):
        """
        Test access to the view for an authenticated user.
        """
        # Verificar el acceso a la vista para un usuario autenticado
        response = self.client.get(reverse('create-event-request'))
        self.assertEqual(response.status_code, 200)

    def test_form_display(self):
        """
        Test correct form display.
        """
        # Verificar que el formulario se muestre correctamente
        response = self.client.get(reverse('create-event-request'))
        self.assertContains(response, '<form', count=1)

    def test_form_submission(self):
        """
        Test form submission.
        """
        # Verificar que el formulario se envíe correctamente
        data = {
            'titulo': 'Test Event',
            'descripcion': 'Description of Test Event',
            'lugar': 'Test Location',
            'fecha_inicio': '2024-05-20',
            'fecha_fin': '2024-05-21',
            'presupuesto': 1000,
            'alimentacion': 'Test Food',
            'transporte': 'Test Transport',
        }
        request = self.factory.post(reverse('create-event-request'), data)
        request.user = self.user  # Establecemos el usuario en el objeto de solicitud

        response = self.client.post(reverse('create-event-request'), data)
        self.assertEqual(response.status_code, 302)  # Redirección después de enviar el formulario

        # Verificar que el evento se haya guardado en la base de datos
        event_requests = EventRequest.objects.filter(usuario=self.user)
        self.assertEqual(event_requests.count(), 1)
        event_request = event_requests.first()

        # Asegúrate de que el evento se cree correctamente
        eventRegistration(request, event_request)

        # Verifica si el evento se creó correctamente
        event = Event.objects.filter(id=event_request.id).first()
        self.assertIsNotNone(event)


class EventListTestCase(TestCase):
    """
    Test cases for listing events.
    """
    def setUp(self):
        """
        Setup method to create test events.
        """
        # Creamos un usuario de prueba y lo autenticamos
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Creamos un grupo
        self.group = Group.objects.create(name='Test Group')
        self.user.groups.add(self.group)# Creamos eventos de prueba
        self.event_1 = Event.objects.create(
            titulo='Evento 1',
            estado_solicitud='En curso',
            fecha_inicio=datetime(2024, 5, 20),
            fecha_fin=datetime(2024, 5, 21),
            presupuesto= "1000",
            alimentacion= "Test Food",
            transporte= 'Test Transport',
        )

        self.event_2 = Event.objects.create(
            titulo='Evento 2',
            estado_solicitud='En curso',
            fecha_inicio=datetime(2024, 5, 22),
            fecha_fin=datetime(2024, 5, 23),
            presupuesto= "1000",
            alimentacion= "Test Food",
            transporte= 'Test Transport',
        )

        self.event_3 = Event.objects.create(
            titulo='Evento 3',
            estado_solicitud='En curso',
            fecha_inicio=datetime(2024, 5, 24),
            fecha_fin=datetime(2024, 5, 25),
            presupuesto= "1000",
            alimentacion= "Test Food",
            transporte= 'Test Transport',
        )

        self.event_4 = Event.objects.create(
            titulo='Evento 4',
            estado_solicitud='Finalizado',
            fecha_inicio=datetime(2024, 5, 26),
            fecha_fin=datetime(2024, 5, 27),
            presupuesto= "1000",
            alimentacion= "Test Food",
            transporte= 'Test Transport',
        )
    def test_access_authenticated_user(self):
        """
        Test access to the view for an authenticated user.
        """
        # Verificar el acceso a la vista para un usuario autenticado
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)

    def test_access_unauthenticated_user(self):
        """
        Test redirection for an unauthenticated user.
        """
        # Verificar que un usuario no autenticado sea redirigido al inicio de sesión
        self.client.logout()
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 302)  # Redirección al inicio de sesión

    def test_event_display(self):
        """
        Test displaying events.
        """
        # Verificar que los eventos se muestren correctamente en la lista
        response = self.client.get(reverse('event-list'))
        self.assertContains(response, 'Evento 1')
        self.assertContains(response, 'Evento 2')
        self.assertContains(response, 'Evento 3')
        self.assertNotContains(response, 'Evento 4')  # El evento 4 no debería estar en la lista


    def test_search_by_nonexistent_title(self):
        """
        Test searching for events with a nonexistent title.
        """
        # Verificar que no se muestren eventos si el título de búsqueda no coincide
        response = self.client.get(reverse('event-list') + '?search=Nonexistent')
        self.assertNotContains(response, 'Evento 1')
        self.assertNotContains(response, 'Evento 2')
        self.assertNotContains(response, 'Evento 3')

    def test_filter_by_status(self):
        """
       Test filtering events by status.
       """
        # Verificar que se puedan filtrar los eventos por estado
        response = self.client.get(reverse('event-list') + '?filter_by=id')
        self.assertContains(response, 'Evento 1')
        self.assertContains(response, 'Evento 2')
        self.assertContains(response, 'Evento 3')
        self.assertNotContains(response, 'Evento 4')  # El evento 4 no debería estar en la lista


class SaveTasksTestCase(TestCase):
    """
    Test cases for saving event tasks.
    """
    def setUp(self):
        """
        Setup method to create a test user and authenticate them, also creates a test event.
        """
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser',email='sacalla3@gmail.com', password='password')
        self.user.email = "sacalla3@gmail.com"  # Establecer el correo electrónico
        self.user.save()

        self.client.login(username='testuser', password='password')

        # Crear un evento de prueba
        self.event = Event.objects.create(titulo='Evento de prueba', estado_solicitud='En curso', fecha_inicio=datetime(2024, 5, 26),
                                          fecha_fin=datetime(2024, 5, 27),
                                          presupuesto= "1000",
                                          alimentacion= "Test Food",
                                          transporte= 'Test Transport',)

    def test_save_tasks(self):
        """
        Test saving event tasks.
        """
        # Datos a enviar en la solicitud POST
        data = {
            'lugar': 'Nuevo lugar',
            'presupuesto': 1500,
            'alimentacion': 'Nueva alimentación',
            'transporte': 'Nuevo transporte',
            'extra': 'Nueva información adicional'
        }

        # Realizar la solicitud POST a la vista saveTasks
        response = self.client.post(reverse('save_tasks', kwargs={'evento_id': self.event.id}), data)

        # Verificar que la redirección ocurra correctamente
        self.assertRedirects(response, reverse('event-list'))

        # Refrescar el objeto de evento desde la base de datos
        self.event.refresh_from_db()

        # Verificar que los datos hayan sido guardados correctamente en el evento
        self.assertEqual(self.event.lugar, 'Nuevo lugar')
        self.assertEqual(self.event.presupuesto, 1500)
        self.assertEqual(self.event.alimentacion, 'Nueva alimentación')
        self.assertEqual(self.event.transporte, 'Nuevo transporte')
        self.assertEqual(self.event.extra, 'Nueva información adicional')


class EventRegistryTestCase(TestCase):
    """
    Test case for the event registry functionality.
    """
    def setUp(self):

        """
        Set up test data including a test user and some sample events.
        """
        # Creamos un usuario de prueba y lo autenticamos
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        # Creamos eventos de prueba
        self.event_1 = Event.objects.create(
            titulo='Evento 1',
            estado_solicitud='Finalizado',
            fecha_inicio=datetime(2024, 5, 26),
            fecha_fin=datetime(2024, 5, 27),
            presupuesto=1000,
            alimentacion='Test Food',
            transporte='Test Transport'
        )
        self.event_2 = Event.objects.create(
            titulo='Evento 2',
            estado_solicitud='Finalizado',
            fecha_inicio=datetime(2024, 5, 26),
            fecha_fin=datetime(2024, 5, 27),
            presupuesto=1000,
            alimentacion='Test Food',
            transporte='Test Transport'
        )
        self.event_3 = Event.objects.create(
            titulo='Evento 3',
            estado_solicitud='Finalizado',
            fecha_inicio=datetime(2024, 5, 26),
            fecha_fin=datetime(2024, 5, 27),
            presupuesto=1000,
            alimentacion='Test Food',
            transporte='Test Transport'
        )
        self.event_4 = Event.objects.create(
            titulo='Evento 4',
            estado_solicitud='En curso',
            fecha_inicio=datetime(2024, 5, 26),
            fecha_fin=datetime(2024, 5, 27),
            presupuesto=1000,
            alimentacion='Test Food',
            transporte='Test Transport'
        )


        # Creamos un factory para las solicitudes
        self.factory = RequestFactory()

    def test_access(self):
        """
        Test access to the event registry view.
        """

        # Verificar el acceso a la vista
        response = self.client.get(reverse('event-registry'))
        self.assertEqual(response.status_code, 200)

    def test_list_finished_events(self):
        """
        Test listing only finished events in the event registry.
        """
        # Verificar que solo se muestren los eventos finalizados
        response = self.client.get(reverse('event-registry'))
        eventos = response.context['eventos']
        self.assertEqual(eventos.count(), 3)  # Deberían haber 3 eventos finalizados

    def test_search_by_id(self):
        """
        Test searching events by ID in the event registry.
        """
        # Verificar la búsqueda por ID
        url = reverse('event-registry') + '?search=1&filter_by=id'
        response = self.client.get(url)
        eventos = response.context['eventos']
        self.assertEqual(eventos.count(), 1)  # Debería haber solo 1 evento con ID 1

    def test_search_by_title(self):
        """
        Test searching events by title in the event registry.
        """
        # Verificar la búsqueda por título
        url = reverse('event-registry') + '?search=Evento&filter_by=titulo'
        response = self.client.get(url)
        eventos = response.context['eventos']
        self.assertEqual(eventos.count(), 3)  # Deberían haber 3 eventos que contengan "Evento" en el título

class ResetCeremonyTestCase(TestCase):
    """
        Test case for resetting ceremony functionality.
        """
    def setUp(self):

        """
        Set up test data including a test user.
        """
        # Creamos un usuario de prueba y lo autenticamos
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_reset_ceremony_post(self):
        """
        Test resetting ceremony via POST request.
        """
        # Creamos algunas actividades de ceremonia
        CeremonyActivity.objects.create(title='Actividad 1')
        CeremonyActivity.objects.create(title='Actividad 2')

        # Realiza una solicitud POST para restablecer la ceremonia
        response = self.client.post(reverse('reset_ceremony'))

        # Verifica que se haya realizado una redirección
        self.assertEqual(response.status_code, 302)

        # Sigue la redirección
        response = self.client.get(response.url)




    def test_reset_ceremony_get(self):
        """
        Test resetting ceremony via GET request.
        """
        # Enviamos una solicitud GET (no debería tener ningún efecto)
        response = self.client.get(reverse('reset_ceremony'))

        # Verificamos que no se haya eliminado ninguna actividad de ceremonia
        self.assertEqual(CeremonyActivity.objects.count(), 0)

        # Verificamos que no se haya creado ni reiniciado la ceremonia
        with self.assertRaises(Ceremony.DoesNotExist):
            Ceremony.objects.get(title="Ceremonia de grado")

        # Verificamos que se haya redirigido a la página de planificación de la ceremonia
        self.assertRedirects(response, reverse('ceremony-plan'))

    def test_access_for_unauthenticated_users(self):
        """
        Test access to the ceremony planning page for unauthenticated users.
        """
        response = self.client.get(reverse('ceremony-plan'))
        self.assertEqual(response.status_code, 200)  # Redirige a la página de inicio de sesión

    def test_access_for_authenticated_users(self):
        """
        Test access to the ceremony planning page for authenticated users.
        """
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('ceremony-plan'))
        self.assertEqual(response.status_code, 200)  # Acceso permitido para usuarios autenticados



class GuardarEventoTestCase(TestCase):
    """
    Test case for saving events.
    """
    def setUp(self):

        """
        Set up test data including a test user and a sample event.
        """
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.event = Event.objects.create(titulo='Evento de prueba', estado_solicitud='En curso', fecha_inicio=datetime(2024, 5, 26),
                                          fecha_fin=datetime(2024, 5, 27),
                                          presupuesto=1000,
                                          alimentacion='Test Food',
                                          transporte='Test Transport')

    def test_guardar_evento(self):
        """
        Test saving an event.
        """
        data = {
            'event_id': self.event.id,
            'estado_alimentacion': 'on',
            'estado_transporte': 'on',
            'estado_extras': 'on'
        }
        response = self.client.post(reverse('guardar_evento'), data)
        self.event.refresh_from_db()
        self.assertTrue(self.event.estado_alimentacion)
        self.assertTrue(self.event.estado_transporte)
        self.assertTrue(self.event.estado_extras)
        # Verificar la redirección adecuada después de guardar
        self.assertRedirects(response, reverse('event-list'))


class EventListApoyoTestCase(TestCase):
    """
    Test case for the event list support functionality.
    """
    def setUp(self):
        """
        Set up test data including a test user and some sample events.
        """
        # Crear eventos de prueba
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        Event.objects.create(titulo='Evento 1', estado_solicitud='En curso', fecha_inicio=datetime(2024, 5, 26),
                             fecha_fin=datetime(2024, 5, 27),
                             presupuesto=1000,
                             alimentacion='Test Food',
                             transporte='Test Transport')
        Event.objects.create(titulo='Evento 2', estado_solicitud='Finalizado', fecha_inicio=datetime(2024, 5, 26),
                             fecha_fin=datetime(2024, 5, 27),
                             presupuesto=1000,
                             alimentacion='Test Food',
                             transporte='Test Transport')
        Event.objects.create(titulo='Evento 3', estado_solicitud='En curso', fecha_inicio=datetime(2024, 5, 26),
                             fecha_fin=datetime(2024, 5, 27),
                             presupuesto=1000,
                             alimentacion='Test Food',
                             transporte='Test Transport')

    def test_event_list_apoyo(self):
        """
           Test displaying the event list support view.
           """
        response = self.client.get(reverse('event-list-apoyo'))
        self.assertEqual(response.status_code, 200)
        eventos = response.context['eventos']
        # Verificar que solo se muestren los eventos con estado 'En curso'
        self.assertEqual(len(eventos), 2)

class FinishEventApoyoTestCase(TestCase):
    """
   Test cases for finishing events for support staff.
   """

    def setUp(self):
        """
        Setup method to create test events.
        """
        # Crear eventos de prueba
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

        Event.objects.create(titulo='Evento 1', estado_solicitud='En curso', fecha_inicio=datetime(2024, 5, 26),
                             fecha_fin=datetime(2024, 5, 27),
                             presupuesto=1000,
                             alimentacion='Test Food',
                             transporte='Test Transport')
        Event.objects.create(titulo='Evento 2', estado_solicitud='Finalizado', fecha_inicio=datetime(2024, 5, 26),
                             fecha_fin=datetime(2024, 5, 27),
                             presupuesto=1000,
                             alimentacion='Test Food',
                             transporte='Test Transport')
        Event.objects.create(titulo='Evento 3', estado_solicitud='Finalizado', fecha_inicio=datetime(2024, 5, 26),
                             fecha_fin=datetime(2024, 5, 27),
                             presupuesto=1000,
                             alimentacion='Test Food',
                             transporte='Test Transport')

    def test_finish_event_apoyo(self):
        """
        Test finishing events for support staff.
        """
        response = self.client.get(reverse('finish-event-apoyo'))
        self.assertEqual(response.status_code, 200)
        eventos = response.context['eventos']
        # Verificar que solo se muestren los eventos con estado 'Finalizado'
        self.assertEqual(len(eventos), 2)
