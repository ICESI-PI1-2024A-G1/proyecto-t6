
from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import EventRequest
from myapp.models import Notification


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
            profesor='Prof. Smith',
            extra='Información adicional'  # Añadir el campo extra
        )
        self.assertEqual(
            str(solicitud),
            "Usuario: testuser, Lugar: Tokio, Fecha de inicio: 2024-04-01, Fecha de fin: 2024-04-05, Presupuesto: 1500, Alimentación: Incluida, Transporte: Autobús, Profesor: Prof. Smith, Estado: Pendiente, Extra: Información adicional"
        )

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

class NotificationTestCase(TestCase):
    def setUp(self):
         # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_creacion_notificacion(self):
        notificacion = Notification.objects.create(
            user=self.user,
            message='Hola, mundo'
        )
        self.assertEqual(
            str(notificacion),
            "Hola, mundo"
        )

    def test_editar_notificacion(self):
        # Crear una notificación
        notificacion = Notification.objects.create(user=self.user, message='Mensaje original')

        # Editar el mensaje de la notificación
        notificacion.message = 'Mensaje modificado'
        notificacion.save()

        # Verificar que el mensaje se haya modificado correctamente
        self.assertEqual(notificacion.message, 'Mensaje modificado')

    def test_eliminar_notificacion(self):
        # Crear una notificación
        notificacion = Notification.objects.create(user=self.user, message='Mensaje a eliminar')

        # Guardar el ID de la notificación
        notificacion_id = notificacion.id

        # Eliminar la notificación
        notificacion.delete()

        # Verificar que la notificación haya sido eliminada correctamente
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(id=notificacion_id)