import os
import uuid

from django.db import models
from user.models import User


def post_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{uuid.uuid4()}{extension}"

    return os.path.join("uploads/post/image", filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to=post_image_file_path)

    def __str__(self):
        return self.title


class Commentary(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.owner.email


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like")

    class Meta:
        unique_together = (
            "owner",
            "post",
        )

    def __str__(self):
        return self.owner.pk
