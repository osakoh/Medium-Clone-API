from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "title",
        "slug",
        "banner_image",
        "show_tags",
        "views",
        "pkid",
        "id",
    ]
    list_filter = ["author", "title", "slug", "views"]
    list_display_links = ["author", "title", "slug", "show_tags", "views"]

    def show_tags(self, obj):
        """
        self: the class name. i.e. articles.ArticleAdmin
        self: reps the string representation defined in the model. E.g timz's article

        iterates over tags in the M2M relationship
        """
        # get the list of tags
        tags = [tag.tag for tag in obj.tags.all()]
        # join all tags using a new line as a separator; causing each tag to be printed on a new line
        tags = ",\n".join(tags)
        return tags
