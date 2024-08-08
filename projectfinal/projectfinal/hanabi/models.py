from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models

# Create your models here.

class User(AbstractUser):
    pass

class Game(models.Model):
    name = models.CharField(max_length=25)
    started = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField()
    score = models.PositiveSmallIntegerField(default=0,validators=[MaxValueValidator(25)])
    hints = models.PositiveSmallIntegerField(default=8,validators=[MaxValueValidator(8)])
    fuses = models.PositiveSmallIntegerField(default=3,validators=[MaxValueValidator(3)])

class Deck(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    cards = models.JSONField()

class GamePlayer(models.Model):
    player = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    hand = models.JSONField()
