from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followees = models.ManyToManyField("self", through='Follower', symmetrical=False, related_name="followers")


class Follower(models.Model):
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'follower')
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'followee')

    class Meta:
        unique_together = ('follower', 'followee')


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return f"{self.user}, {self.timestamp}, {self.content}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }


class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

