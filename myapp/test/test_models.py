
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import EventRequest

class EventRequestTestCase(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_creacion_solicitud_evento(self):
        solicitud = EventRequest.objects.create(
            usuario=self.user,
            lugar='Tokio',
            fecha_inicio='2024-04-01',
            fecha_fin='2024-04-05',
            presupuesto=1500,
            alimentacion='Incluida',
            transporte='Autobús',
            profesor='Prof. Smith'
        )
        self.assertEqual(str(solicitud), "Usuario: testuser, Lugar: Tokio, Fecha de inicio: 2024-04-01, Fecha de fin: 2024-04-05, Presupuesto: 1500, Alimentación: Incluida, Transporte: Autobús, Profesor: Prof. Smith, Estado: Pendiente")

    def test_asignacion_profesor(self):
        solicitud = EventRequest.objects.create(usuario=self.user, lugar='Kioto', fecha_inicio='2024-04-10', fecha_fin='2024-04-15', presupuesto=2000, alimentacion='No incluida', transporte='Tren')
        solicitud.profesor = 'Prof. Johnson'
        solicitud.save()
        self.assertEqual(solicitud.profesor, 'Prof. Johnson')

    def test_cambio_estado_solicitud(self):
        solicitud = EventRequest.objects.create(usuario=self.user, lugar='Osaka', fecha_inicio='2024-05-01', fecha_fin='2024-05-05', presupuesto=1800, alimentacion='Incluida', transporte='Avión')
        solicitud.estado_solicitud = 'Aprobado'
        solicitud.save()
        self.assertEqual(solicitud.estado_solicitud, 'Aprobado')
