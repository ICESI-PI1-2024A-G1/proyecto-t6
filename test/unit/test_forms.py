import unittest
from django.test import TestCase
from myapp.forms import EventRequestForm, EstadoSolicitudForm, CeremonyActivityForm, EventRequest
from datetime import datetime


class TestEventRequestForm(TestCase):
    """
    Test suite for the event request form.

    Scenario:
    This test suite evaluates the functionality of the event request form, ensuring that it behaves correctly under various scenarios.

    """

    def test_missing_required_fields(self):
        """
        Test that the form returns errors when required fields are missing.

        Scenario:
        This test case verifies that the form correctly identifies missing required fields and returns errors accordingly.

        """

        form_data = {}  # Empty data
        form = EventRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [
            'None of the fields can be empty.'])

    def test_invalid_date_range(self):
        """
        Test that the form returns errors when the date range is invalid.

        Scenario:
        This test case checks if the form detects an invalid date range and returns errors appropriately.

        """

        form_data = {
            'lugar': 'Conference Hall',
            # Start date after end date
            'fecha_inicio': datetime(2024, 4, 3),
            'fecha_fin': datetime(2024, 4, 1),
            'presupuesto': 1000,
            'alimentacion': True,
            'transporte': False,
            'profesor': 'John Doe'
        }
        form = EventRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [
            'Start date cannot be after end date.'])

    def test_negative_budget(self):
        """
        Test that the form returns errors when the budget is negative.

        Scenario:
        This test case ensures that the form properly handles negative budget values and returns errors accordingly.

        """

        form_data = {
            'lugar': 'Conference Hall',
            'fecha_inicio': datetime(2024, 4, 1),
            'fecha_fin': datetime(2024, 4, 3),
            'presupuesto': -100,  # Negative budget
            'alimentacion': True,
            'transporte': False,
            'profesor': 'John Doe'
        }
        form = EventRequestForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], [
            'Budget cannot be negative.'])

    def test_valid_data(self):
        """
        Test that the event request form accepts valid data.

        Scenario:
        This test case verifies that the form accepts valid data without raising any errors.

        """

        form_data = {
            'evento_id': 1,
            'estado_solicitud': 'approved'
        }
        form = EstadoSolicitudForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_event_request(self):
        """
        Test that an event request can be created successfully.

        Scenario:
        This test case verifies that an event request can be created successfully using the form.

        """

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
        """
        Test that an event request can be edited successfully.

        Scenario:
        This test case verifies that an existing event request can be edited successfully using the form.

        """

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
        """
        Test that an event request can be deleted successfully.

        Scenario:
        This test case verifies that an existing event request can be deleted successfully.

        """

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
        """
        Test that a status request can be created successfully.

        Scenario:
        This test case verifies that a status request can be created successfully using the form.

        """

        form_data = {
            'evento_id': 1,
            'estado_solicitud': 'pending'
        }
        form = EstadoSolicitudForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_ceremony_activity(self):
        """
        Test that a ceremony activity can be created successfully.

        Scenario:
        This test case verifies that a ceremony activity can be created successfully using the form.

        """

        form_data = {
            'title': 'Test Activity'
        }
        form = CeremonyActivityForm(data=form_data)
        self.assertTrue(form.is_valid())

