from django.test import TestCase
from django.contrib.auth.models import User
from myapp.models import Professor, EventRequest, Event, Notification, Ceremony, CeremonyActivity


class TestCreateModels(TestCase):
    """
    Test case for creating instances of various models.
    """
    def setUp(self):
        """
        Set up initial data for each test method.
        """
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_create_professor(self):
        professor = Professor.objects.create(name='John Doe', email='john@example.com')
        self.assertEqual(Professor.objects.count(), 1)

    def test_create_event_request(self):
        event_request = EventRequest.objects.create(
            usuario=self.user,
            titulo='Test Event',
            descripcion='Description of test event',
            lugar='Test Location',
            fecha_inicio='2024-05-10',
            fecha_fin='2024-05-12',
            presupuesto=1000,
            alimentacion='Yes',
            transporte='No',
            estado_solicitud='Pending',
            extra='Extra information'
        )
        self.assertEqual(EventRequest.objects.count(), 1)

    def test_create_event(self):
        event = Event.objects.create(
            usuario=self.user,
            titulo='Test Event',
            descripcion='Description of test event',
            lugar='Test Location',
            fecha_inicio='2024-05-10',
            fecha_fin='2024-05-12',
            presupuesto=1000,
            alimentacion='Yes',
            transporte='No',
            estado_solicitud='In progress',
            extra='Extra information',
            estado_alimentacion=True,
            estado_transporte=False,
            estado_extras=True
        )
        self.assertEqual(Event.objects.count(), 1)

    def test_create_notification(self):
        notification = Notification.objects.create(message='Test Notification', url='http://example.com')
        self.assertEqual(Notification.objects.count(), 1)

    def test_create_ceremony(self):
        ceremony = Ceremony.objects.create(title='Test Ceremony', start_date='2024-06-01', end_date='2024-06-05')
        self.assertEqual(Ceremony.objects.count(), 1)

    def test_create_ceremony_activity(self):
        ceremony = Ceremony.objects.create(title='Test Ceremony', start_date='2024-06-01', end_date='2024-06-05')
        ceremony_activity = CeremonyActivity.objects.create(title='Test Activity', ceremony=ceremony)
        self.assertEqual(CeremonyActivity.objects.count(), 1)

    """
    Test case for editing instances of various models.
    """

    def setUp(self):
        """
       Set up initial data for each test method.
       """
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.professor = Professor.objects.create(name='John Doe', email='john@example.com')
        self.event_request = EventRequest.objects.create(
            usuario=self.user,
            titulo='Test Event',
            descripcion='Description of test event',
            lugar='Test Location',
            fecha_inicio='2024-05-10',
            fecha_fin='2024-05-12',
            presupuesto=1000,
            alimentacion='Yes',
            transporte='No',
            estado_solicitud='Pending',
            extra='Extra information'
        )
        self.event = Event.objects.create(
            usuario=self.user,
            titulo='Test Event',
            descripcion='Description of test event',
            lugar='Test Location',
            fecha_inicio='2024-05-10',
            fecha_fin='2024-05-12',
            presupuesto=1000,
            alimentacion='Yes',
            transporte='No',
            estado_solicitud='In progress',
            extra='Extra information',
            estado_alimentacion=True,
            estado_transporte=False,
            estado_extras=True
        )
        self.notification = Notification.objects.create(message='Test Notification', url='http://example.com')
        self.ceremony = Ceremony.objects.create(title='Test Ceremony', start_date='2024-06-01', end_date='2024-06-05')
        self.ceremony_activity = CeremonyActivity.objects.create(title='Test Activity', ceremony=self.ceremony)

    def test_edit_professor(self):
        self.professor.name = 'Jane Doe'
        self.professor.save()
        self.assertEqual(Professor.objects.get(pk=self.professor.pk).name, 'Jane Doe')

    def test_edit_event_request(self):
        self.event_request.titulo = 'Edited Test Event'
        self.event_request.save()
        self.assertEqual(EventRequest.objects.get(pk=self.event_request.pk).titulo, 'Edited Test Event')

    def test_edit_event(self):
        self.event.titulo = 'Edited Test Event'
        self.event.save()
        self.assertEqual(Event.objects.get(pk=self.event.pk).titulo, 'Edited Test Event')

    def test_edit_notification(self):
        self.notification.message = 'Edited Test Notification'
        self.notification.save()
        self.assertEqual(Notification.objects.get(pk=self.notification.pk).message, 'Edited Test Notification')

    def test_edit_ceremony(self):
        self.ceremony.title = 'Edited Test Ceremony'
        self.ceremony.save()
        self.assertEqual(Ceremony.objects.get(pk=self.ceremony.pk).title, 'Edited Test Ceremony')

    def test_edit_ceremony_activity(self):
        self.ceremony_activity.title = 'Edited Test Activity'
        self.ceremony_activity.save()
        self.assertEqual(CeremonyActivity.objects.get(pk=self.ceremony_activity.pk).title, 'Edited Test Activity')


    """
    Test case for deleting instances of various models.
    """
    def setUp(self):
        """
        Set up initial data for each test method.
        """
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.professor = Professor.objects.create(name='John Doe', email='john@example.com')
        self.event_request = EventRequest.objects.create(
            usuario=self.user,
            titulo='Test Event',
            descripcion='Description of test event',
            lugar='Test Location',
            fecha_inicio='2024-05-10',
            fecha_fin='2024-05-12',
            presupuesto=1000,
            alimentacion='Yes',
            transporte='No',
            estado_solicitud='Pending',
            extra='Extra information'
        )
        self.event = Event.objects.create(
            usuario=self.user,
            titulo='Test Event',
            descripcion='Description of test event',
            lugar='Test Location',
            fecha_inicio='2024-05-10',
            fecha_fin='2024-05-12',
            presupuesto=1000,
            alimentacion='Yes',
            transporte='No',
            estado_solicitud='In progress',
            extra='Extra information',
            estado_alimentacion=True,
            estado_transporte=False,
            estado_extras=True
        )
        self.notification = Notification.objects.create(message='Test Notification', url='http://example.com')
        self.ceremony = Ceremony.objects.create(title='Test Ceremony', start_date='2024-06-01', end_date='2024-06-05')
        self.ceremony_activity = CeremonyActivity.objects.create(title='Test Activity', ceremony=self.ceremony)

    def test_delete_professor(self):
        self.professor.delete()
        self.assertEqual(Professor.objects.count(), 0)

    def test_delete_event_request(self):
        self.event_request.delete()
        self.assertEqual(EventRequest.objects.count(), 0)

    def test_delete_event(self):
        self.event.delete()
        self.assertEqual(Event.objects.count(), 0)

    def test_delete_notification(self):
        self.notification.delete()
        self.assertEqual(Notification.objects.count(), 0)

    def test_delete_ceremony(self):
        self.ceremony.delete()
        self.assertEqual(Ceremony.objects.count(), 0)

    def test_delete_ceremony_activity(self):
        self.ceremony_activity.delete()
        self.assertEqual(CeremonyActivity.objects.count(), 0)
