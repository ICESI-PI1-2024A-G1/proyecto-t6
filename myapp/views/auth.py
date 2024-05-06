from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect


def academicMembersLogin(request):
    """
    View function for handling the login of academic members.

    Renders the loginAcademicCommunity.html template with the AuthenticationForm
    if the request method is GET. If the request method is POST, it attempts to
    authenticate the user using the provided username and password. If authentication
    is successful and the user belongs to the appropriate group (group 3 or 4), the
    user is logged in and redirected to the index page. Otherwise, an error message
    is rendered indicating incorrect credentials or membership.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered template or a redirect response.
    """
    if request.method == "GET":
        return render(
            request, "loginAcademicCommunity.html", {
                "form": AuthenticationForm}
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
                    "error": "Incorrect username or password!",
                },
            )
        else:
            group = user.groups.values_list('id', flat=True).first()
            print("User ID:", group)
            if (group == 3 or group == 4):
                login(request, user)
                return redirect("index")

            return render(
                request,
                "loginAcademicCommunity.html",
                {
                    "form": AuthenticationForm,
                    "error": "Credentials do not belong to an academic community member!",
                },
            )


def ccsaLogin(request):
    """
    View function for handling the login of CCSA members.

    Renders the CCSAlogin.html template with the AuthenticationForm
    if the request method is GET. If the request method is POST, it attempts to
    authenticate the user using the provided username and password. If authentication
    is successful and the user belongs to the appropriate group (group 1 or 2), the
    user is logged in and redirected to the index page. Otherwise, an error message
    is rendered indicating incorrect credentials or membership.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A rendered template or a redirect response.
    """
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
                    "error": "Incorrect username or password!",
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
                    "error": "Credentials do not belong to a CCSA member!",
                },
            )


def signout(request):
    """
    View function for handling user logout.

    Logs out the user and redirects to the home page.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - A redirect response to the home page.
    """
    logout(request)
    return redirect("home")
