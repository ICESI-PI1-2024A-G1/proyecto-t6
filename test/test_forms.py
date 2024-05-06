import unittest
from django.test import TestCase
from myapp.forms import EventRequestForm, EstadoSolicitudForm
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


class TestEstadoSolicitudForm(TestCase):
    def test_valid_data(self):
        form_data = {
            'evento_id': 1,
            'estado_solicitud': 'aprobada'
        }
        form = EstadoSolicitudForm(data=form_data)
        self.assertTrue(form.is_valid())


if __name__ == '__main__':
    unittest.main()
