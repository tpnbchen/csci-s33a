from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("new_user", views.new_user, name="new_user"),
    path("rules", views.rules, name="rules"),
    path("games", views.games, name="games"),
    path("new_game", views.new_game, name="new_game"),
    path("list_games", views.list_games, name="list_games"),
    path("join_game", views.join_game, name="join_game"),
    path("play_game/<int:game_id>", views.play_game, name="play_game"),
    path("game_state/<int:game_id>", views.game_state, name="game_state")
]