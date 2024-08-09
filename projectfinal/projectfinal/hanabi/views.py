from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.db.models.base import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.urls import reverse

from random import shuffle

from .models import User, Game, GamePlayer, Board

import json

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
        confirmation = request.POST["confirmation"]
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
    ).annotate(
        joined=Count('gameplayer')
    ).order_by(
        "-started"
    ).values(
        "id",
        "name",
        "creator__username",
        "numplayers",
        "joined",
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
        user = request.user,
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
    existing_players = User.objects.filter(gameplayer__game=game)
    filled_spots = GamePlayer.objects.filter(game=game).count()

    # prevent join if player is already in game or game is finished or active
    if (
            request.user not in existing_players and
            game.get_status_display() == 'New'
       ):
        player = GamePlayer(
            user = request.user,
            game = game
        )
        player.save()

        # Start game if fill last spot
        filled_spots = GamePlayer.objects.filter(game=game).count()
        if filled_spots == game.numplayers:
            setup_game(game)
            game.status = game.Status.IN_PROGRESS
            game.save()
            play_game(request, game.id)
            
    else:
        return JsonResponse({"error": "Something went wrong joining the game"}, status=400)
    
    return JsonResponse({"message": "Game joined"}, status=201)


# go to gameplay interface for a specific game
def play_game(request, game_id):
    try:
        game = Game.objects.get(id=game_id, gameplayer__user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse("index")) 

    return render(request, f"hanabi/game.html", {
        "name": game.name,
        "score": game.score,
        "hints": game.hints,
        "fuses": game.fuses,
        # players
    })

# take a turn
def take_turn(request):
    pass

# shuffle deck and deal hands
def setup_game(game):

    # generate board
    # hard coded for now. Create function  to change in future
    COLORS = ("white", "yellow", "green", "blue", "red")
    NUMBERS = 5

    deck = []
    hands = {}
    discard = []
    fireworks = {}
    for color in COLORS:
        fireworks[color] = 0
    gameplayers = GamePlayer.objects.filter(game=game)    

    # randomly determine player order
    player_list = list(gameplayers)
    shuffle(player_list)
    
    for player in player_list:
        order = player_list.index(player)
        player.turn_order = order
        player.save()
        if order == 0:
            starting_player = player

    # generate deck
    for color in COLORS:
        for i in range(1, NUMBERS):
            if i == 1:
                for j in range(3):
                    deck.append({'color': color, "number": f"{i}"})
            elif i in [2, 3, 4]:
                for j in range(2):
                    deck.append({'color': color, "number": f"{i}"})
            else:
                deck.append({'color': color, "number": f"{i}"})
    shuffle(deck)
    
    # deal hands
    if len(gameplayers) in [4, 5]:
        handsize = 4
    else:
        handsize = 5
    for gameplayer in gameplayers:
        hands[gameplayer.user.id] = {}
        for i in range(1, handsize+1):
            card = f"card {i}"
            hands[gameplayer.user.id].update({card: deck.pop()})
            hands[gameplayer.user.id][card].update({"knowledge": 'set()'})

    # save board to db
    board = Board(
        game = game,
        currentPlayer = starting_player.user,
        cards = json.dumps({
            "deck": deck,
            "hands": hands,
            "discard": discard,
            "fireworks": fireworks
        })
    )
    board.save()


# retreive game state
def game_state(request, game_id):
    print("gamestatehere")
    requesting_player = request.user

    # get active game with the requesting player
    game = Game.objects.get(id=game_id)
    gameplayers = GamePlayer.objects.filter(game=game)
    board = Board.objects.get(game=game)
    cards = json.loads(board.cards)

    # get information specific to requesting player
    other_hands = {}
    requesting_player_hand = {}
    for gameplayer in gameplayers:
        if gameplayer.user is not requesting_player:
            other_hands[gameplayer.user.id] = cards['hands'][f"{gameplayer.user.id}"]
        else:
            for card in cards['hands'][gameplayer.user.id]:
                requesting_player_hand[card] = cards['hands'][gameplayer.user.id][card]['knowledge']
    
    # combine all state data to send to client
    state = {
        "score": game.score,
        "fuses": game.fuses,
        "hints": game.hints,
        "deck": cards['deck'],
        "fireworks": cards['fireworks'],
        "discard": cards['discard'],
        "current_player": board.currentPlayer.id,
        "other_hands": other_hands,
        "requesting_player_hand": requesting_player_hand
    }

    return JsonResponse(state, safe=False)
