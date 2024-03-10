from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import academic_members_information
# Create your views here.

def hello(request):
    return HttpResponse("<h1>Hello World<h1>")

def index(request):
    return render(request, 'index.html')

def academicMembersLogin(request):
    if request.method == 'GET':
        return render(request, 'loginAcademicCommunity.html',{
        'form' : AuthenticationForm
        })
    else:
        user = authenticate(
            request, username = request.POST['username'], password = request.POST['password']
        )
        if user is None:
            return render(request, 'loginAcademicCommunity.html', {
            'form' : AuthenticationForm,
            'error' : 'Username or password is incorrect!'
            })
        else:
            login(request, user)
            return redirect('index')
    
    
def signout(request):    
    logout(request)
    return redirect('academicMembersLoginyyy')