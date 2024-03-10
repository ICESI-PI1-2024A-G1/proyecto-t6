from django import forms
from .models import EventRequest

class EventRequestForm(forms.ModelForm):
    class Meta:
        model = EventRequest
        fields = ['lugar', 'fecha_inicio', 'fecha_fin', 'presupuesto', 'alimentacion', 'transporte']
