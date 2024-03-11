from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class EventRequest(models.Model):
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    lugar = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    alimentacion = models.CharField(max_length=200)
    transporte = models.CharField(max_length=200)

    def __str__(self):
        return f'Usuario: {self.usuario}, Lugar: {self.lugar}, Fecha de inicio: {self.fecha_inicio}, Fecha de fin: {self.fecha_fin}, Presupuesto: {self.presupuesto}, Alimentación: {self.alimentacion}, Transporte: {self.transporte}'
