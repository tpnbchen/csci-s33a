from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, related_name="followed_by")


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True,editable=False)

    def __str__(self):
        return f"{self.user}, {self.timestamp}, {self.content}"
    
    def serialize(self):
        return {
            "user": self.user,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)