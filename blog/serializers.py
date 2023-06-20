from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
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
        )
        read_only_fields = ("owner",)
