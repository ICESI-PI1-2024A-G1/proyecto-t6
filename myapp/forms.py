from django import forms
from .models import EventRequest

from django import forms
from .models import EventRequest

class EventRequestForm(forms.ModelForm):
    class Meta:
        model = EventRequest
        fields = ['lugar', 'fecha_inicio', 'fecha_fin', 'presupuesto', 'alimentacion', 'transporte', 'profesor']

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        presupuesto = cleaned_data.get('presupuesto')

        # Validación de campos vacíos
        for field in ['lugar', 'fecha_inicio', 'fecha_fin', 'presupuesto', 'alimentacion', 'transporte', 'profesor']:
            if not cleaned_data.get(field):
                self.add_error(field, "Este campo es requerido.")

        # Validación de fechas
            if fecha_inicio and fecha_fin:
                if fecha_inicio >= fecha_fin:
                    self.add_error('fecha_inicio', "La fecha de inicio debe ser anterior a la fecha de fin.")

            return cleaned_data

class EstadoSolicitudForm(forms.Form):
    evento_id = forms.IntegerField(widget=forms.HiddenInput)
    estado_solicitud = forms.CharField(label='Estado de la Solicitud', widget=forms.Select(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')]))
