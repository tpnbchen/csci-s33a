from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    follows = models.ManyToManyField("self", through='Follower', symmetrical=False, related_name="followed_by")


class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'follower')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'followee')

    class Meta:
        unique_together = ('follower', 'followee')


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return f"{self.user}, {self.timestamp}, {self.content}"


class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
