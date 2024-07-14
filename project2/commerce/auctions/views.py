from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.base import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewListingForm
from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.all()
    highest_bids = {}
    for listing in listings:
        try:
            highest_bid = Bid.objects.filter(listing=listing).order_by("amount")[0]
        except IndexError:
            highest_bid = 0
        if highest_bid > listing.starting_bid:
            highest_bids[listing] = highest_bid
        else:
            highest_bids[listing] = listing.starting_bid
    return render(request, "auctions/index.html", {
            "listings": highest_bids
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# create a new listing
@login_required
def listing_new(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image_link = form.cleaned_data["image_link"]
            starting_bid = form.cleaned_data["starting_bid"]
            category = form.cleaned_data["category"]
            listing = Listing(
                user=request.user, title=title, description=description, 
                starting_bid=starting_bid,image_link=image_link, category=category)
            listing.save()
            return listing_view(request, listing.id)
        else:
            return render(request, "auctions/listing_new.html", {
                "form": form,
                "errors": form.errors
            })
    else:
        return render(request, "auctions/listing_new.html", {
            "form": NewListingForm()
        })


# render an existing listing
def listing_view(request, listing_id):
    try:
        listing = Listing.objects.get(id=listing_id)
    except ObjectDoesNotExist:
        return listingNotFound(request, listing_id)
    
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

@login_required
def listing_delete(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if request.user == listing.user:
        listing.delete()
    return HttpResponseRedirect(reverse("index"))


def watchlist(request):
    pass


def categories(request):
    pass


# helper function to display listing not found page
def listingNotFound(request, listing_id):
    return render(request, "auctions/listing404.html", {
            "listing_id": listing_id
        })