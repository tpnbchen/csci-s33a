from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing_new", views.listing_new, name="listing_new"),
    path("listing_view/<int:listing_id>", views.listing_view, name="listing_view"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>", views.watchlist, name="watchlist"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("categories", views.categories, name="categories"),
    path("category", views.category, name="category"),
    path("category/<str:name>", views.category, name="category"),
    path("comment/<int:listing_id>", views.comment, name="comment")
]
