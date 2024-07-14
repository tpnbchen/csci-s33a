from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(primary_key=True, max_length=32)


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    starting_bid = models.PositiveIntegerField()
    image_link = models.URLField(blank=True, null=True)
    category = models.ForeignKey(Category, 
            on_delete=models.SET_NULL, blank=True, null=True)


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField()
    submitted = models.DateTimeField(auto_now_add=True, editable=False)


class Comment(models.Model):
    pass

