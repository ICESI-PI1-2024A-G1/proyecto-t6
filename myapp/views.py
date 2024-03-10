from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import academy_Users_Credentials

#<} Create your views here.

def index(request):
    return render(request, 'index.html')

def academicUsersLogin(request):
    if request.method == 'GET':
        return render(request, 'loginAcademyComunity.html',{
        'form' : AuthenticationForm
        })
    else:
        user = authenticate(
            request, username = request.POST['username'], password = request.POST['password']
        )
        if user is None:
            return render(request, 'loginAcademyComunity.html', {
            'form' : AuthenticationForm,
            'error' : 'Username or password incorrect!'
            })
        else:
            login(request, user)
            return redirect('index')
    
    
def signout(request):    
    logout(request)
    return redirect('academicUsersLogin')

