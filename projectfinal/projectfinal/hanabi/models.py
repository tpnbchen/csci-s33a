from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    pass

class Game(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    started = models.DateTimeField(auto_now_add=True)
    numplayers = models.PositiveSmallIntegerField(default=2,validators=[MinValueValidator(2), MaxValueValidator(5)])
    score = models.PositiveSmallIntegerField(default=0,validators=[MaxValueValidator(25)])
    hints = models.PositiveSmallIntegerField(default=8,validators=[MaxValueValidator(8)])
    fuses = models.PositiveSmallIntegerField(default=3,validators=[MaxValueValidator(3)])
    
    class Status(models.IntegerChoices):
        NEW = 1, _("New")
        IN_PROGRESS = 2, _("In Progress")
        FINISHED = 3, _("Finished")

    status = models.PositiveBigIntegerField(choices=Status, default=Status.NEW)
    
class Board(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    cards = models.JSONField(null=True)
    currentPlayer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # board format:


class GamePlayer(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    turn_order = models.PositiveBigIntegerField(null=True)