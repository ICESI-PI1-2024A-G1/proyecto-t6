from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from .forms import EventRequestForm
from .models import EventRequest


class CreateEventRequestViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_get_request(self):
        response = self.client.get(reverse('create-event-request'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EventRequestForm)

    def test_post_valid_form(self):
        form_data = {
            'lugar': 'Sala de conferencias',
            'fecha_inicio': '2024-04-01',
            'fecha_fin': '2024-04-03',
            'presupuesto': 1000,
            'alimentacion': True,
            'transporte': False,
            'profesor': 'Juan Pérez'
        }
        response = self.client.post(reverse('create-event-request'), data=form_data)
        self.assertEqual(response.status_code, 302)  # Debe redireccionar después de un POST válido
        self.assertEqual(EventRequest.objects.count(), 1)  # Debe haber una solicitud de evento creada
        self.assertEqual(EventRequest.objects.first().usuario, self.user)  # El usuario debe ser el mismo que inició sesión

        # Verificar mensaje de éxito
        storage = get_messages(response.wsgi_request)
        self.assertEqual(len(storage), 1)
        self.assertEqual(str(storage[0]), 'Se ha creado una solicitud de evento: <EventRequest: Solicitud de evento en Sala de conferencias>')

    def test_post_invalid_form(self):
        # Enviar datos inválidos para el formulario (sin lugar)
        form_data = {
            'fecha_inicio': '2024-04-01',
            'fecha_fin': '2024-04-03',
            'presupuesto': 1000,
            'alimentacion': True,
            'transporte': False,
            'profesor': 'Juan Pérez'
        }
        response = self.client.post(reverse('create-event-request'), data=form_data)
        self.assertEqual(response.status_code, 200)  # El formulario es inválido, debe permanecer en la misma página
        self.assertEqual(EventRequest.objects.count(), 0)  # No debe haber solicitud de evento creada

        # Verificar que el formulario sea enviado de vuelta con errores
        self.assertIn('Este campo es requerido.', response.content.decode())

    def tearDown(self):
        self.client.logout()
