import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.urls import reverse

from .models import User, Game, GamePlayer, Deck

def index(request):
    return render(request, "hanabi/index.html")


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
        return render(request, "hanabi/login.html")


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
            return render(request, "hanabi/new_user.html", {
                "message": "Passwords do not match."
            })
        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "hanabi/new_user.html", {
                "message": "Username already exists."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "hanabi/new_user.html")


# rules page
def rules(request):
    return render(request, "hanabi/rules.html")

# games page
def games(request):
    return render(request, "hanabi/games.html")

# get list of new games
def list_games(request):
    games = Game.objects.filter(
        status=Game.Status.NEW
    ).order_by(
        "-started"
    ).values(
        "id",
        "name",
        "creator__username",
        "numplayers",
        "started"
    )
    response = {}
    response['games_list'] = list(games)
    return JsonResponse(response, safe=False)

# create a new game
def new_game(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    game_name = data.get("game_name")
    numplayers = data.get("numplayers")

    new_game = Game(
        name = game_name,
        creator = request.user,
        numplayers = numplayers
    )
    new_game.save()

    player_1 = GamePlayer(
        player = request.user,
        game = new_game
    )
    player_1.save()

    return JsonResponse({"message": "New Game created"}, status=201)


# join a game
def join_game(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    requested_game = data.get("game")
    requested_game_id = requested_game["id"]
    game = Game.objects.get(id=requested_game_id)
    existing_players = User.objects.filter(gameplayer__player=request.user, gameplayer__game=game)
    filled_spots = GamePlayer.objects.filter(game=game).count()

    # prevent join if player is already in game or game is finished or active
    if (
            request.user not in existing_players and
            game.get_status_display() == 'New'
       ):
        player = GamePlayer(
            player = request.user,
            game = game
        )
        player.save()

        # Start game if fill last spot
        filled_spots = GamePlayer.objects.filter(game=game).count()
        if filled_spots == game.numplayers:
            game.status = game.Status.IN_PROGRESS
            game.save()
            play_game()
        print("cannot join")


    return JsonResponse({"message": "Game joined"}, status=201)

# go to gameplay interface for a specific game
def game(game):
    pass

# take a turn
def take_turn(request):
    pass

