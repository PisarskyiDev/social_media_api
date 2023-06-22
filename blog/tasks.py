# Create your tasks here

# from blog.models import
# TODO: add usable model

from celery import shared_task


@shared_task
def generate_new_post():
    return 5 + 5
