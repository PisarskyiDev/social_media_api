from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from blog.models import Post, Commentary, Like
from blog.serializers import (
    PostSerializer,
    CommentarySerializer,
    LikeSerializer,
    PostListSerializer,
    CommentaryListSerializer,
)
from user.permissions import IsOwnerOrAdminOrReadOnly


class PostViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Post.objects.all().select_related("owner").prefetch_related("comments", "like")
    )
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentaryViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly)

    def get_serializer_class(self):
        if self.action == "list":
            return CommentaryListSerializer
        return CommentarySerializer

    def get_queryset(self):
        return Commentary.objects.filter(
            post__pk=self.kwargs["post_pk"]
        ).prefetch_related("owner")

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        serializer.save(owner=self.request.user, post=post)


class LikeViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    model = Like
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdminOrReadOnly)

    def get_queryset(self):
        return Like.objects.filter(post__pk=self.kwargs["post_pk"])

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs["post_pk"])
        try:
            serializer.save(owner=self.request.user, post=post)
        except IntegrityError:
            raise PermissionDenied("You can like a post only once.")
