from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as sub_routers
from blog.views import PostViewSet, CommentaryViewSet, LikeViewSet

app_name = "blog"

router = routers.DefaultRouter()
router.register("posts", PostViewSet)

posts_router = sub_routers.NestedSimpleRouter(router, "posts", lookup="post")
posts_router.register("commentary", CommentaryViewSet, basename="post-commentaries")
posts_router.register("like", LikeViewSet, basename="post-like")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(posts_router.urls)),
]
