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
    profesor = models.CharField(null=True, max_length=200)
    estado_solicitud = models.CharField(null=True, max_length=200, default='Pendiente')
    extra = models.CharField(null = True, max_length = 200)
    
    def __str__(self):
        return f'Usuario: {self.usuario}, Lugar: {self.lugar}, Fecha de inicio: {self.fecha_inicio}, Fecha de fin: {self.fecha_fin}, Presupuesto: {self.presupuesto}, Alimentación: {self.alimentacion}, Transporte: {self.transporte}, Profesor: {self.profesor}, Estado: {self.estado_solicitud}, Extra: {self.extra}'
    
class Event(models.Model):
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    lugar = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    alimentacion = models.CharField(max_length=200)
    transporte = models.CharField(max_length=200)
    profesor = models.CharField(null=True, max_length=200)
    extra = models.CharField(null = True, max_length = 200)

    def __str__(self):
        return f'Usuario: {self.usuario}, Lugar: {self.lugar}, Fecha de inicio: {self.fecha_inicio}, Fecha de fin: {self.fecha_fin}, Presupuesto: {self.presupuesto}, Alimentación: {self.alimentacion}, Transporte: {self.transporte}, Profesor: {self.profesor}, Extra: {self.extra}'
