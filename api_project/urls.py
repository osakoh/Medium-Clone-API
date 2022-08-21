from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Blog API",
        default_version="v1",
        description="API endpoints for the Blog API",
        contact=openapi.Contact(email="macmive@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # drf-yasg urls
    path(
        "api/v1/docs/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    # admin site urls
    path(settings.ADMIN_URL, admin.site.urls),
    # djoser urls =>
    path("api/v1/auth/", include("djoser.urls")),
    # djoser jwt urls
    path("api/v1/auth/jwt/", include("djoser.urls.jwt")),
    # profiles urls
    path("api/v1/profiles/", include("main_apps.profiles.urls")),
    # articles urls
    path("api/v1/articles/", include("main_apps.articles.urls")),
    # ratings urls
    path("api/v1/ratings/", include("main_apps.ratings.urls")),
    # reactions urls
    path("api/v1/vote/", include("main_apps.reactions.urls")),
    # favorites urls
    path("api/v1/favorite/", include("main_apps.favorites.urls")),
    # comments urls
    path("api/v1/comments/", include("main_apps.comments.urls")),
    # search urls
    path("api/v1/haystack/", include("main_apps.search.urls")),
]

# customise Admin site header, title etc
admin.site.site_header = "Blog API Admin"
admin.site.site_title = "Admin Portal for Blog API"
admin.site.index_title = "Admin Portal: Blog API"
