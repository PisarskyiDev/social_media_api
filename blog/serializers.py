from rest_framework import serializers

from blog.models import Post, Commentary, Like


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


class CommentaryListSerializer(CommentarySerializer):
    class Meta:
        model = Commentary
        fields = (
            "id",
            "owner",
        )
        read_only_fields = (
            "owner",
            "post",
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "id",
            "owner",
        )
        read_only_fields = (
            "owner",
            "post",
        )


class PostSerializer(serializers.ModelSerializer):
    comments = CommentaryListSerializer(many=True, read_only=True)
    like = LikeSerializer(many=True, read_only=True)
    image = serializers.ImageField(use_url=True, allow_null=True, required=False)

    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "title",
            "content",
            "created_at",
            "updated_at",
            "image",
            "comments",
            "like",
        )
        read_only_fields = ("owner",)

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "image" and value is None:
                continue
            setattr(instance, attr, value)
        instance.save()
        return instance


class PostListSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "title",
            "content",
            "created_at",
            "updated_at",
            "image",
        )
        read_only_fields = ("owner",)
