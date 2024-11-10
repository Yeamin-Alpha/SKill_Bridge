from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField()
    num_comments = models.IntegerField(default=0)
    num_upvotes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post by {self.user.username} - Upvotes: {self.num_upvotes}"

