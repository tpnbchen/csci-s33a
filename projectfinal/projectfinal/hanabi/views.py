from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse

from .models import User

def index(request):
    return HttpResponse("hello world!")


# login
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponse(reverse("index"))
        else:
            return render(request, "hanabi/login.html", {
                "message": "invalid username and/or password"
            })
    else:
        return render(request, "hanabi.login.html")


# logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# new user
def new_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        password = request.POST["password"]
        confirmation = request.POST["password"]
        if confirmation != password: 
            return render(request, "network/register.html", {
                "message": "Passwords do not match."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already exists."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# rules page
def rules(request):
    return HttpResponse("Rules")


# start a new game
def start_game(request):
    pass


# join a game
def join_game(request):
    pass


# take a turn
def take_turn(request):
    pass