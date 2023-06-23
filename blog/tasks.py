import random
from blog.models import Post
from user.models import User
from celery import shared_task


@shared_task
def generate_random_post():
    words = [
        "Lorem",
        "Ipsum",
        "Dolor",
        "Sit",
        "Amet",
        "Consectetur",
        "Adipiscing",
        "Elit",
    ]

    title = " ".join(random.choices(words, k=5))

    content = " ".join(random.choices(words, k=50))

    owner = User.objects.order_by("?").first()

    Post.objects.create(title=title, content=content, owner=owner)
