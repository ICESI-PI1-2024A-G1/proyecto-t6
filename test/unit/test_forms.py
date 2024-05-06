import unittest
from django.test import TestCase
from myapp.forms import EventRequestForm, EstadoSolicitudForm, CeremonyActivityForm, EventRequest
from datetime import datetime


class TestEventRequestForm(TestCase):

    def test_missing_required_fields(self):
        form_data = {}  # Datos vacíos
        form = EventRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [
                         'Ninguno de los campos puede estar vacío.'])

    def test_invalid_date_range(self):
        form_data = {
            'lugar': 'Sala de conferencias',
            # Fecha de inicio después de la fecha de fin
            'fecha_inicio': datetime(2024, 4, 3),
            'fecha_fin': datetime(2024, 4, 1),
            'presupuesto': 1000,
            'alimentacion': True,
            'transporte': False,
            'profesor': 'Juan Pérez'
        }
        form = EventRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [
                         'La fecha de inicio no puede ser posterior a la fecha de fin.'])

    def test_negative_budget(self):
        form_data = {
            'lugar': 'Sala de conferencias',
            'fecha_inicio': datetime(2024, 4, 1),
            'fecha_fin': datetime(2024, 4, 3),
            'presupuesto': -100,  # Presupuesto negativo
            'alimentacion': True,
            'transporte': False,
            'profesor': 'Juan Pérez'
        }
        form = EventRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [
                         'El presupuesto no puede ser negativo.'])



    def test_valid_data(self):
        form_data = {
            'evento_id': 1,
            'estado_solicitud': 'aprobada'
        }
        form = EstadoSolicitudForm(data=form_data)
        self.assertTrue(form.is_valid())


    if __name__ == '__main__':
        unittest.main()

    def test_create_event_request(self):
        form_data = {
            'titulo': 'Test Event',
            'descripcion': 'Description of test event',
            'lugar': 'Test Location',
            'fecha_inicio': datetime(2024, 5, 10),
            'fecha_fin': datetime(2024, 5, 12),
            'presupuesto': 1000,
            'alimentacion': 'Yes',
            'transporte': 'No',
            'profesor': None
        }
        form = EventRequestForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_edit_event_request(self):
        # Create an event request instance
        event_request = EventRequest.objects.create(
            titulo='Test Event',
            descripcion='Description of test event',
            lugar='Test Location',
            fecha_inicio='2024-05-10',
            fecha_fin='2024-05-12',
            presupuesto=1000,
            alimentacion='Yes',
            transporte='No'
        )

        # Prepare form data for editing
        form_data = {
            'titulo': 'Updated Test Event',
            'descripcion': 'Updated description of test event',
            'lugar': 'Updated Test Location',
            'fecha_inicio': datetime(2024, 5, 15),
            'fecha_fin': datetime(2024, 5, 17),
            'presupuesto': 1500,
            'alimentacion': 'No',
            'transporte': 'Yes',
            'profesor': None
        }

        # Get the form instance for editing
        form = EventRequestForm(data=form_data, instance=event_request)
        self.assertTrue(form.is_valid())

    def test_delete_event_request(self):
        # Create an event request instance
        event_request = EventRequest.objects.create(
            titulo='Test Event',
            descripcion='Description of test event',
            lugar='Test Location',
            fecha_inicio='2024-05-10',
            fecha_fin='2024-05-12',
            presupuesto=1000,
            alimentacion='Yes',
            transporte='No'
        )

        # Delete the event request
        event_request.delete()

        # Check if the event request has been deleted
        self.assertEqual(EventRequest.objects.count(), 0)

    def test_create_estado_solicitud(self):
        form_data = {
            'evento_id': 1,
            'estado_solicitud': 'pendiente'
        }
        form = EstadoSolicitudForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_ceremony_activity(self):
        form_data = {
            'title': 'Test Activity'
        }
        form = CeremonyActivityForm(data=form_data)
        self.assertTrue(form.is_valid())
