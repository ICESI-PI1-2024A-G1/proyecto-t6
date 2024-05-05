from django.views.generic.list import ListView
from myapp.models import EventRequest

class calendar(ListView):
    model = EventRequest
    template_name = "calendar.html"
    
    def get_queryset(self):
        """
        Get the classes associated with a given teacher ID.

        Returns:
        list: List of dictionaries containing class information.
        """
        # Get the classes associated with a given teacher
        queryset = self.model.objects.filter(estado_solicitud = "aprobada").all()
        print(queryset)
        # Initialize the array of out
        out = []
        # Get the most important information of the classes
        for event in queryset:
            out.append({
                'start': event.fecha_inicio.strftime('%Y-%m-%d'),
                'end': event.fecha_fin.strftime('%Y-%m-%d')
            })
        return out