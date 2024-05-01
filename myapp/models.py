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
    profesor = models.ForeignKey(
        Professor, null=True, blank=True, on_delete=models.SET_NULL)
    estado_solicitud = models.CharField(
        null=True, max_length=200, default='Pendiente')
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
    profesor = models.ForeignKey(
        Professor, null=True, on_delete=models.SET_NULL)
    estado_solicitud = models.CharField(
        null=True, max_length=200, default='En curso')
    extra = models.CharField(blank=True, null=True, max_length=200)

    def __str__(self):
        return f'Usuario: {self.usuario}, Lugar: {self.lugar}, Fecha de inicio: {self.fecha_inicio}, Fecha de fin: {self.fecha_fin}, Presupuesto: {self.presupuesto}, Alimentación: {self.alimentacion}, Transporte: {self.transporte}, Profesor: {self.profesor}, Estado: {self.estado_solicitud}, Extra: {self.extra}'


class Notification(models.Model):
    message = models.TextField()
    url = models.CharField(null=True, max_length=200, blank=True)

    def _str_(self):
        return self.message


class Ceremony(models.Model):
    title = models.CharField(max_length=200, default="Ceremonia de grado")
    start_date = models.DateField(default="2024-01-01")
    end_date = models.DateField(default="2024-01-01")

    def __str__(self):
        return self.title


class CeremonyActivity(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    ceremony = models.ForeignKey(
        Ceremony, null=True, default=1, on_delete=models.CASCADE, related_name='ceremony_activities')

    def __str__(self):
        return self.title
