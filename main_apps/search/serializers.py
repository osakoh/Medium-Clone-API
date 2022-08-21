from drf_haystack.serializers import HaystackSerializer

from main_apps.search.search_indexes import ArticleIndex


class ArticleSearchSerializer(HaystackSerializer):
    class Meta:
        # The `index_classes` attribute is a list of which search indexes to be included in the search.
        index_classes = [ArticleIndex]

        # The `fields` contains all the fields to be included.
        # These fields belong to the search index (ArticleIndex) and not a model
        fields = ["author", "title", "body", "autocomplete", "created_at", "updated_at"]

        #  tells the REST framework to ignore these fields. Used when you do not want
        #  to serialize and transfer the content of a text, or n-gram index down to the client
        ignore_fields = ["autocomplete"]

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=oslo would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {"q": "autocomplete"}
