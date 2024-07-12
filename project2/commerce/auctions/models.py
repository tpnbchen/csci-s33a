from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    title = models.CharField()
    description = models.CharField()
    image_link = models.URLField()


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    amount = models.PositiveIntegerField()


class Comment(models.Model):
    pass



