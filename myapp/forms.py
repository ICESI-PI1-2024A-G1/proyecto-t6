from django import forms
from .models import EventRequest

from django import forms
from .models import EventRequest

class EventRequestForm(forms.ModelForm):
    class Meta:
        model = EventRequest
        fields = ['lugar', 'fecha_inicio', 'fecha_fin', 'presupuesto', 'alimentacion', 'transporte', 'profesor']


class EstadoSolicitudForm(forms.Form):
    evento_id = forms.IntegerField(widget=forms.HiddenInput)
    estado_solicitud = forms.CharField(label='Estado de la Solicitud', widget=forms.Select(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')]))
