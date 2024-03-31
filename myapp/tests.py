import unittest
from django.test import TestCase
from .forms import EventRequestForm, EstadoSolicitudForm

class TestEventRequestForm(TestCase):
    def test_valid_data(self):
        form_data = {
            'lugar': 'Sala de conferencias',
            'fecha_inicio': '2024-04-01',
            'fecha_fin': '2024-04-03',
            'presupuesto': 1000,
            'alimentacion': True,
            'transporte': False,
            'profesor': 'Juan Pérez'
        }
        form = EventRequestForm(data=form_data)
        self.assertTrue(form.is_valid())
