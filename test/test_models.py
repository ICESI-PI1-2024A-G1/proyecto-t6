import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import EventRequest


class EventRequestTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_cambio_estado_solicitud(self):
        solicitud = EventRequest.objects.create(usuario=self.user, lugar='Osaka', fecha_inicio='2024-05-01',
                                                fecha_fin='2024-05-05', presupuesto=1800, alimentacion='Incluida', transporte='Avión')
        solicitud.estado_solicitud = 'Aprobado'
        solicitud.save()
        self.assertEqual(solicitud.estado_solicitud, 'Aprobado')
