from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def index(request):
    group = request.user.groups.values_list("id", flat=True).first()
    firstName = None
    if request.user.is_authenticated:
        firstName = request.user.first_name

    if group == 1:
        return render(request, "index1.html", {'first_name': firstName})
    if group == 2:
        return render(request, "index2.html", {'first_name': firstName})
    return render(request, "index3.html", {'first_name': firstName})