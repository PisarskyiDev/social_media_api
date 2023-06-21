from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from blog.models import Post, Commentary
from blog.serializers import PostSerializer, CommentarySerializer
from user.permissions import IsOwnerOrAdminOrReadOnly


class PostViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Post.objects.all().prefetch_related("comments")
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentaryViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = CommentarySerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly)

    def get_queryset(self):
        return Commentary.objects.filter(post__pk=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(owner=self.request.user, post=post)
