from .models import Notification

def notificaciones(request):
    notificaciones = Notification.objects.all().order_by('-id')[:10]  # Obtener las 10 últimas notificaciones
    return {'notificaciones': notificaciones}
