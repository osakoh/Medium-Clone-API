from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from main_apps.articles.models import Article
from main_apps.articles.serializers import ArticleCreateSerializer

from .exceptions import AlreadyFavorited
from .models import Favorite
from .serializers import FavoriteSerializer


class FavoriteAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoriteSerializer

    """
        def post(self, request, slug):
        data = request.data
        article = Article.objects.get(slug=slug)
        user = request.user
        favorite = Favorite.objects.filter(user=user, article=article.pkid).first()
    """

    def post(self, request, *args, **kwargs):
        data = request.data
        # retrieve slug from keyword argument
        slug = self.kwargs.get("slug")
        article = Article.objects.get(slug=slug)
        user = request.user

        print(
            "\n***************************** In favorites.FavoriteAPIView *********************************"
        )
        print(f"data: {data}")
        print(f"slug: {slug}")
        print(f"article: {article}")
        print(f"user: {user}")
        print(
            "***************************** In favorites.FavoriteAPIView *********************************\n"
        )

        favorite = Favorite.objects.filter(user=user, article=article.pkid).first()

        if favorite:
            raise AlreadyFavorited
        else:
            data["article"] = article.pkid
            data["user"] = user.pkid
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            data = serializer.data
            data["message"] = "Article added to favorites."
            return Response(data, status=status.HTTP_201_CREATED)


class ListUserFavoriteArticlesAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user_id=request.user.pkid)

        favorite_articles = []

        for favorite in favorites:
            article = Article.objects.get(pkid=favorite.article.pkid)
            article = ArticleCreateSerializer(
                article, context={"article": article.slug, "request": request}
            ).data
            favorite_articles.append(article)

        favorites_data = {"my_favorites": favorite_articles}

        return Response(data=favorites_data, status=status.HTTP_200_OK)
