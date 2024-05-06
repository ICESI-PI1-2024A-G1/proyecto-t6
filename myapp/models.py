from django.db import models
from django.contrib.auth.models import User


class Professor(models.Model):
    """
    Model representing a professor.
    """
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        """
        String representation of the model.
        """
        return self.name


class EventRequest(models.Model):
    """
    Model representing an event request.
    """
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=300)
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
        """
        String representation of the model.
        """
        return f'Usuario: {self.usuario}, Lugar: {self.lugar}, Fecha de inicio: {self.fecha_inicio}, Fecha de fin: {self.fecha_fin}, Presupuesto: {self.presupuesto}, Alimentación: {self.alimentacion}, Transporte: {self.transporte}, Profesor: {self.profesor}, Estado: {self.estado_solicitud}, Extra: {self.extra}'


class Event(models.Model):
    """
    Model representing an event.
    """
    usuario = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=300)
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

    estado_alimentacion = models.BooleanField(null=True, blank=True)
    estado_transporte = models.BooleanField(null=True, blank=True)
    estado_extras = models.BooleanField(null=True, blank=True)

    def __str__(self):
        """
        String representation of the model.
        """
        return f'Usuario: {self.usuario}, Lugar: {self.lugar}, Fecha de inicio: {self.fecha_inicio}, Fecha de fin: {self.fecha_fin}, Presupuesto: {self.presupuesto}, Alimentación: {self.alimentacion}, Transporte: {self.transporte}, Profesor: {self.profesor}, Estado: {self.estado_solicitud}, Extra: {self.extra}'


class Notification(models.Model):
    """
    Model representing a notification.
    """
    message = models.TextField()
    url = models.CharField(null=True, max_length=200, blank=True)

    def _str_(self):
        """
        String representation of the model.
        """
        return self.message


class Ceremony(models.Model):
    """
    Model representing a ceremony.
    """
    title = models.CharField(max_length=200, default="Ceremonia de grado")
    start_date = models.DateField(default="2024-01-01")
    end_date = models.DateField(default="2024-01-01")

    def __str__(self):
        """
        String representation of the model.
        """
        return self.title


class CeremonyActivity(models.Model):
    """
    Model representing an activity in a ceremony.
    """
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    ceremony = models.ForeignKey(
        Ceremony, null=True, default=1, on_delete=models.CASCADE, related_name='ceremony_activities')

    def __str__(self):
        """
        String representation of the model.
        """
        return self.title
