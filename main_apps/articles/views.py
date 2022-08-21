import logging

from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from main_apps.articles.models import Article, ArticleViews

from .exceptions import UpdateArticle
from .filters import ArticleFilter
from .pagination import ArticlePagination
from .permissions import IsOwnerOrReadOnly
from .renderers import ArticleJSONRenderer, ArticlesJSONRenderer
from .serializers import (
    ArticleCreateSerializer,
    ArticleSerializer,
    ArticleUpdateSerializer,
)

User = get_user_model()

logger = logging.getLogger(__name__)


class ArticleListAPIView(generics.ListAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Article.objects.all()
    renderer_classes = (ArticlesJSONRenderer,)
    pagination_class = ArticlePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ArticleFilter
    ordering_fields = ["created_at", "username"]


class ArticleCreateAPIView(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = ArticleCreateSerializer
    renderer_classes = [ArticleJSONRenderer]

    def create(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        # set the author of the article to the logged-in user's pkid(UUID)
        data["author"] = user.pkid

        serializer = self.serializer_class(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # logging
        logger.info(
            f"article {serializer.data.get('title')} created by {user.username}"
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailView(APIView):
    """
    Displays the details of an Article
    Increases the view count in ArticleView when a user view an Article detail
    """

    renderer_classes = [ArticleJSONRenderer]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        article = Article.objects.get(slug=slug)
        """
        X-Forwarded-For Header:a request type header and is an alternative version of the Forwarded header
        used when a client connects to a web server through an HTTP proxy or load balancer for identifying 
        the original IP address. The privacy of the user is put at risk as the sensitive information is 
        revealed by using this header. 
        The HTTP X-Forwarded-For header is used to identify the client’s original IP address. 
        The modified version of the HTTP X-Forwarded-For is HTTP Forwarded header.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        # get logged-in users' ip address
        if x_forwarded_for:
            # split on comma and return the first element in the list
            ip = x_forwarded_for.split(",")[0]
        else:
            # REMOTE_ADDR – The IP address of the client
            ip = request.META.get("REMOTE_ADDR")

        # if user hasn't viewed the Article detail
        if not ArticleViews.objects.filter(article=article, ip=ip).exists():
            # add the article viewed & ip address to the ArticleView table
            ArticleViews.objects.create(article=article, ip=ip)

            # increment the view
            article.views += 1
            # save article
            article.save()

        serializer = ArticleSerializer(article, context={"request": request})

        # logging
        logger.info(
            f"user [{request.user}] viewed Article [{serializer.data.get('title')}]"
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([permissions.IsAuthenticated])
def update_article_api_view(request, slug):
    """Updates an Article"""

    # try to retrieve an Article
    try:
        article = Article.objects.get(slug=slug)
    # raise article do note
    except Article.DoesNotExist:
        raise NotFound("Article does not exist")

    user = request.user
    if article.author != user:
        # logging
        logger.info(
            f"user [{request.user}] tried updating an Article [{article.title}] that doesn't belong to them"
        )
        raise UpdateArticle

    #  partial update to the Article
    if request.method == "PATCH":
        data = request.data
        serializer = ArticleUpdateSerializer(article, data=data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ArticleDeleteAPIView(generics.DestroyAPIView):
    """Deletes an Article. User must be authenticated and own the Article"""

    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Article.objects.all()
    lookup_field = "slug"

    def delete(self, request, *args, **kwargs):
        # try to retrieve an Article
        try:
            article = Article.objects.get(slug=self.kwargs.get("slug"))
        # raise article do note
        except Article.DoesNotExist:
            raise NotFound("That article does not exist in our catalog")

        # delete Article
        delete_operation = self.destroy(request)

        data = {}

        # Article was deleted
        if delete_operation:
            # set a success key and value message
            data["success"] = "Deletion was successful"
        # set a failure key and value message
        else:
            data["failure"] = "Deletion failed"

        # return data
        return Response(data=data)
