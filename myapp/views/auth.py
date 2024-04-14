from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect

def academicMembersLogin(request):
    if request.method == "GET":
        return render(
            request, "loginAcademicCommunity.html", {"form": AuthenticationForm}
        )
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "loginAcademicCommunity.html",
                {
                    "form": AuthenticationForm,
                    "error": "Nombre de usuario o contraseña incorrecta!",
                },
            )
        else:
            group = user.groups.values_list('id', flat=True).first()
            print("ID del usuario:", group)
            if (group==3 or group==4):
                login(request, user)
                return redirect("index")

            return render(
                request,
                "loginAcademicCommunity.html",
                {
                    "form": AuthenticationForm,
                    "error": "Las credenciales no son de un mienbro la comunidad!",
                },
            )


def ccsaLogin(request):
    if request.method == "GET":
        return render(request, "CCSAlogin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "CCSAlogin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Nombre de usuario o contraseña incorrecta!",
                },
            )
        else:
            group = user.groups.values_list("id", flat=True).first()
            if group == 1 or group == 2:
                login(request, user)
                return redirect("index")

            return render(
                request,
                "CCSAlogin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Las credenciales no son de un miembro de la CCSA!",
                },
            )


def signout(request):
    logout(request)
    return redirect("home")