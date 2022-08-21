import django_filters as filters

from main_apps.articles.models import Article


class ArticleFilter(filters.FilterSet):
    author = filters.CharFilter(
        field_name="author__first_name", lookup_expr="icontains"
    )
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.CharFilter(
        field_name="tags", method="get_article_tags", lookup_expr="iexact"
    )
    created_at = filters.IsoDateTimeFilter(field_name="created_at")
    updated_at = filters.IsoDateTimeFilter(field_name="updated_at")

    class Meta:
        model = Article
        fields = ["author", "title", "tags", "created_at", "updated_at"]

    # method="get_article_tags"
    def get_article_tags(self, queryset, tags, value):
        # replace spaces with no-space and spilt on comma
        tag_values = value.replace(" ", "").split(",")
        # return queryset of distinct tags based on what the user in searching for

        print(
            "\n******************************* In articles.filters ****************************************"
        )
        print(f"queryset : {queryset}")
        print(f"tags : {tags}")
        print(f"value : {value}")
        print(
            f"queryset.filter(tags__tag__in=tag_values).distinct() : "
            f"{queryset.filter(tags__tag__in=tag_values).distinct()}"
        )
        print(
            "******************************* In articles.filters ****************************************\n"
        )

        return queryset.filter(tags__tag__in=tag_values).distinct()
