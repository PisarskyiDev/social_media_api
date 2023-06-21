from rest_framework import serializers

from blog.models import Post, Commentary


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = (
            "id",
            "owner",
            "post",
            "content",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "owner",
            "post",
        )


class CommentaryToPostSerializer(CommentarySerializer):
    class Meta:
        model = Commentary
        fields = (
            "id",
            "owner",
            "post",
        )
        read_only_fields = (
            "owner",
            "post",
        )


class PostSerializer(serializers.ModelSerializer):
    comments = CommentaryToPostSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "title",
            "content",
            "image",
            "created_at",
            "updated_at",
            "comments",
        )
        read_only_fields = ("owner",)
