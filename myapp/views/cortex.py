from django.shortcuts import render
from django.views.generic.list import ListView
from myapp.models import Event


class cortex(ListView):

    model = Event
    template_name = "index1.html"

    def home(request):
        return render(request, "home.html")

    def index(request):
        group = request.user.groups.values_list("id", flat=True).first()
        firstName = None
        if request.user.is_authenticated:
            firstName = request.user.first_name

        if group == 1:
            template_name = "index1.html"
            return render(request, "index1.html", {'first_name': firstName})
        if group == 2:
            return render(request, "index2.html", {'first_name': firstName})

        return render(request, "index3.html", {'first_name': firstName})

    def get_queryset(self):
        """
        Get the classes associated with a given teacher ID.

        Returns:
        list: List of dictionaries containing class information.
        """
        # Get the classes associated with a given teacher
        queryset = self.model.objects.filter(estado_solicitud="En curso").all()
        print(queryset)
        # Initialize the array of out
        out = []
        # Get the most important information of the classes
        for event in queryset:
            out.append({
                'title': event.titulo,
                'start': event.fecha_inicio.strftime('%Y-%m-%d'),
                'end': event.fecha_fin.strftime('%Y-%m-%d')
            })
        return out
