from django.contrib.auth.models import AbstractUser
from django.db import models

# Table of Users
class User(AbstractUser):
    pass

# Table of Category options for Listings
class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=32)


# Table of Listings
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.PositiveIntegerField()
    image_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, 
            on_delete=models.SET_NULL, blank=True, null=True)


# Table of Bids
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField()
    submitted = models.DateTimeField(auto_now_add=True, editable=False)


# Table of Comments
class Comment(models.Model):
    pass


# Association table between user and listing
class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)