from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["pkid", "id", "article", "author", "body"]
    list_filter = ["pkid", "id", "article", "author", "body"]
    list_display_links = ["pkid", "id", "article", "author", "body"]
