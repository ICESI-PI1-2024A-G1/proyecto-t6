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
        request_start_date = cleaned_data.get('request_start_date')
        request_end_date = cleaned_data.get('request_end_date')
        request_budget = cleaned_data.get('request_budget')

        # Validación de campos vacíos
        for field in ['request_place', 'request_start_date', 'request_end_date', 'request_budget', 'request_supply', 'request_transport', 'request_professor']:
            if not cleaned_data.get(field):
                self.add_error(field, "Este campo es requerido.")

        # Validación de fechas
            if request_start_date and request_end_date:
                if request_start_date >= request_end_date:
                    self.add_error('request_start_date', "La fecha de inicio debe ser anterior a la fecha de fin.")

            return cleaned_data

class EstadoSolicitudForm(forms.Form):
    evento_id = forms.IntegerField(widget=forms.HiddenInput)
    estado_solicitud = forms.CharField(label='Estado de la Solicitud', widget=forms.Select(choices=[('pendiente', 'Pendiente'), ('aprobada', 'Aprobada'), ('rechazada', 'Rechazada')]))
