from django.shortcuts import render
from django.views.generic.list import ListView
from myapp.models import Event


class cortex(ListView):
    """
    A ListView-based class to display events in different templates based on user groups.
    """

    model = Event
    template_name = "index1.html"

    def home(request):
        """
        Renders the home page template.
        """
        return render(request, "home.html")

    def index(request):
        """
        Renders different templates based on the user group:
        - Template index1.html for group 1 users.
        - Template index2.html for group 2 users.
        - Template index3.html for users not belonging to groups 1 or 2.
        """
        group = request.user.groups.values_list("id", flat=True).first()
        firstName = None

        queryset = Event.objects.filter(estado_solicitud="En curso").all()
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

        if request.user.is_authenticated:
            firstName = request.user.first_name

        if group == 1:
            template_name = "index1.html"
            return render(request, "index1.html", {'first_name': firstName, 'object_list':out})
        if group == 2:
            return render(request, "index2.html", {'first_name': firstName, 'object_list':out})

        return render(request, "index3.html", {'first_name': firstName})
