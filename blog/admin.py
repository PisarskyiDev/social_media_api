from django.contrib import admin
from django.contrib.auth.models import Group

from blog.models import Post, Commentary


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "created_at",
        "updated_at",
        "owner",
    )
    search_fields = (
        "title",
        "owner__email",
    )
    ordering = ("-created_at",)


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = (
        "owner",
        "post",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "owner__email",
        "post__title",
    )
    ordering = ("-created_at",)


admin.site.unregister(Group)
