from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as net_routers
from blog.views import PostViewSet, CommentaryViewSet

app_name = "blog"

router = routers.SimpleRouter()
router.register("posts", PostViewSet)

posts_router = net_routers.NestedSimpleRouter(router, "posts", lookup="post")
posts_router.register("commentary", CommentaryViewSet, basename="post-commentaries")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_router.urls)),
]
