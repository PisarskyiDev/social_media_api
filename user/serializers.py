from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "is_staff",
            "sex",
            "subscribe",
            "followers",
            "avatar",
        )
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    @staticmethod
    def get_followers(obj):
        """Filter out followers, except current user"""
        followers = obj.followers.exclude(pk=obj.pk)
        return [follower.pk for follower in followers]

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password and avatar correctly and return it"""
        password = validated_data.pop("password", None)
        avatar = validated_data.pop("avatar", None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)

        if avatar is not None:
            user.avatar = avatar

        user.save()

        return user


class UserCreateSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "sex", "avatar")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
