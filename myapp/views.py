from django.shortcuts import render
from .models import Project, Tast
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .forms import CreateNewTask

# Create your views here.


def index(request):
    return render(request, 'index.html')


def hello(request, username):
    print(username)
    return HttpResponse("<h1>Hello %s</h1>" % username)


def about(request):
    return HttpResponse("About")


def projects(request):
    # projects = list(Project.objects.all().values())
    projects = Project.objects.all()

    return render(request, 'projects.html', {
        'projects': projects
    })


def tasks(request, id):
    task = get_object_or_404(Tast, id=id)
    return HttpResponse('task: %s' % task.tittle)


def create_task(request):
    if request.method == 'GET':
        return render(request,  'create_task.html', {
            'form': CreateNewTask()
        })
    else:
        Tast.objects.create(
            tittle=request.GET['tittle'], description=request.GET['description'], project_id=1)
        return
