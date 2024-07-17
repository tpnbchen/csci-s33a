from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models.base import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import NewListingForm, WatchListForm, BidForm, CloseForm, CommentForm
from .models import User, Listing, Bid, Comment, WatchlistItem, Category


# show active listings
def index(request):

    # get all listings and associated highest bids
    listings = Listing.objects.all()
    highest_bids = {}
    for listing in listings:
        bid = bid_highest(listing.id)
        if bid:
            highest_bids[listing] = bid.amount
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


# logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# register user account
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


# create a new Listing
@login_required
def listing_new(request):

    # submitting a new Listing
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            image_link = form.cleaned_data["image_link"]
            starting_bid = form.cleaned_data["starting_bid"]
            category = form.cleaned_data["category"]

            # create Listing
            listing = Listing(
                    user=request.user, title=title, description=description,
                    starting_bid=starting_bid, image_link=image_link,
                    category=category)
            listing.save()
            return listing_view(request, listing.id)

        # if form data is not valid
        else:
            error(request, form.errors)

    # view new Listing form
    else:
        return render(request, "auctions/listing_new.html", {
            "form": NewListingForm()
        })


# view an existing listing
def listing_view(request, listing_id, message=""):

    # get Listing from database
    try:
        listing = listing_get(listing_id)
    except ObjectDoesNotExist:
        return error(request, "listing not found")

    # get WatchListItem
    try:
        watchlistitem = WatchlistItem.objects.get(
                listing__id=listing_id, user__username=request.user)
    except ObjectDoesNotExist:
        watchlistitem = None

    # get Comments
    try:
        comments = Comment.objects.filter(
                listing__id=listing_id).order_by("-submitted")
    except ObjectDoesNotExist:
        comments = []

    # get current Bid
    bid = bid_highest(listing_id)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "message": message,
        "bid": bid,
        "comments": comments,
        "watchlistitem": watchlistitem,
        "watchlistform": WatchListForm(initial={"listing": listing_id}),
        "bidform": BidForm(),
        "closeform": CloseForm(initial={"closed": True}),
        "commentform": CommentForm()
    })


# add a comment to Listing
@login_required
def comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            comment = Comment(
                    user=request.user, listing=listing_get(listing_id),
                    text=text)
            comment.save()
            return HttpResponseRedirect(
                    reverse("listing_view", args=[listing_id]))
        else:
            error(request, form.errors)
    else:
        return HttpResponseRedirect(reverse("listing_view", args=[listing_id]))


# View, add, remove Listing from Watchlist
@login_required
def watchlist(request, listing_id=""):

    # submit Watchlist update
    if request.method == "POST":
        form = WatchListForm(request.POST)
        if form.is_valid():
            # not using form data to retrieve the listing and using
            # URL parameter instead, not sure which is better

            # remove Listing from Watchlist if already added
            try:
                watchlistitem = WatchlistItem.objects.get(
                        listing__id=listing_id, user__username=request.user)
                watchlistitem.delete()
            # add Listing to Watchlist if not
            except ObjectDoesNotExist:
                watchlistitem = WatchlistItem(
                        user=request.user, listing=listing_get(listing_id))
                watchlistitem.save()
            return listing_view(request, listing_id, "Watchlist updated")

        # if form data is invalid
        else:
            error(request, form.errors)

    # show Watchlist page
    else:
        watchlistitems = request.user.watchlist.all()
        listings = []
        for item in watchlistitems:
            listings.append(item.listing)
        return render(request, "auctions/watchlist.html", {
            "listings": listings
        })


@login_required
def bid(request, listing_id):
    listing = listing_get(listing_id)
    bid = bid_highest(listing_id)

    # check if there have been any bids
    if bid:
        bid_amount = bid.amount
    else:
        bid_amount = listing.starting_bid

    # take bid submission
    if request.method == "POST" and listing.closed is not True:
        form = BidForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data["amount"]

        # save bid submission if it is highest
        if amount > bid_amount:
            bid = Bid(user=request.user, listing=listing, amount=amount)
            bid.save()
            return listing_view(
                    request, listing_id, f"Bid submitted: {amount}")
        else:
            return listing_view(
                request, listing_id,
                f"Your bid must be higher than current bid: {bid_amount}")
    else:
        return HttpResponseRedirect(reverse("listing_view", args=[listing_id]))


# close Listing
@login_required
def close(request, listing_id):
    listing = listing_get(listing_id)
    if (request.method == "POST" and
            listing.closed is not True and
            listing.user == request.user):
        listing.closed = True
        listing.save()
        return listing_view(request, listing_id, "Listing closed")
    else:
        return HttpResponseRedirect(reverse("listing_view", args=[listing_id]))


# view list of Categories
@login_required
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


# view Listings for a Category
@login_required
def category(request, name=""):
    if name == "":
        filter = None
    else:
        filter = name
    listings = Listing.objects.filter(category=filter)
    return render(request, "auctions/category.html", {
        "category": name,
        "listings": listings
    })


# helper function to display error page
def error(request, errors="something went wrong"):
    return render(request, "auctions/error.html", {
                    "errors": errors
                })


# helper function to get highest Bid for Listing
def bid_highest(listing_id):
    listing = listing_get(listing_id)

    # find highest bid if any
    try:
        bid = Bid.objects.filter(listing__id=listing_id).order_by("-amount")[0]

        # in case a bid lower than the starting bid gets submitted
        if bid.amount > listing.starting_bid:
            return bid
    except IndexError:
        return None


# helper function to get Listing from listing id
def listing_get(listing_id):
    listing = Listing.objects.get(id=listing_id)
    return listing
