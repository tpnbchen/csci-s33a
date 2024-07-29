
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profile>", views.profile, name="profile"),
    path("get_posts", views.get_posts, name="get_posts"),
    path("post", views.post, name="post"),
    path("follow_status", views.follow_status, name="follow_status"),
    path("like", views.like, name="like"),
    path("edit", views.edit, name="edit"),
    path("following", views.following, name="following")
]
