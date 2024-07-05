from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/page", views.page, name="page"),
    path("wiki/<str:title>", views.entry, name="entry")
]

