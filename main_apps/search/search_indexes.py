from django.utils import timezone
from haystack import indexes

from main_apps.articles.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    # indicates to Haystack & the search engine to know the primary field
    text = indexes.CharField(document=True)
    author = indexes.CharField(model_attr="author")
    title = indexes.CharField(model_attr="title")
    body = indexes.CharField(model_attr="body")
    created_at = indexes.CharField(model_attr="created_at")
    updated_at = indexes.CharField(model_attr="updated_at")

    @staticmethod
    def prepare_author(obj):
        return "" if not obj.author else obj.author.username

    @staticmethod
    def prepare_autocomplete(obj):
        return " ".join((obj.author.username, obj.title, obj.description))

    def get_model(self):
        """Model to be indexed"""
        return Article

    def index_queryset(self, using=None):
        """
        used when the entire index for model is updated

        A common theme is to allow admin users to add future content but have it not display on the site until
        that future date is reached. A custom index_queryset method prevents those future Articles from being indexed.
        """
        return self.get_model().objects.filter(created_at__lte=timezone.now())
