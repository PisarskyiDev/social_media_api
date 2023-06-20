from django.urls import path, include
from rest_framework import routers

from blog.views import PostViewSet

app_name = "blog"

router = routers.DefaultRouter()
router.register("posts", PostViewSet, basename="posts")

urlpatterns = [
    path("", include(router.urls)),
]
