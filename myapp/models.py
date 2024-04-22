# models.py

from django.db import models
from django.contrib.auth.models import User

class Professor(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class EventRequest(models.Model):
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    lugar = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    alimentacion = models.CharField(max_length=200)
    transporte = models.CharField(max_length=200)
    profesor = models.ForeignKey(Professor, null=True, blank=True, on_delete=models.SET_NULL)
    estado_solicitud = models.CharField(null=True, max_length=200, default='Pendiente')
    extra = models.CharField(null=True, blank=True, max_length=200)

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
    profesor = models.ForeignKey(Professor, null=True, on_delete=models.SET_NULL)
    extra = models.CharField(blank=True, null=True, max_length = 200)

    def __str__(self):
        return f'Usuario: {self.usuario}, Lugar: {self.lugar}, Fecha de inicio: {self.fecha_inicio}, Fecha de fin: {self.fecha_fin}, Presupuesto: {self.presupuesto}, Alimentación: {self.alimentacion}, Transporte: {self.transporte}, Profesor: {self.profesor}, Extra: {self.extra}'

class Notification(models.Model):
    message = models.TextField()
    def __str__(self):
        return self.message