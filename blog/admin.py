from django.contrib import admin
from django.contrib.auth.models import Group

from blog.models import Post


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


admin.site.unregister(Group)
