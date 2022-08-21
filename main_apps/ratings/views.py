from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from main_apps.articles.models import Article

from .exceptions import AlreadyRated, CantRateYourArticle
from .models import Rating


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_article_rating_view(request, article_id):
    author = request.user
    article = Article.objects.get(id=article_id)
    data = request.data

    if article.author == author:
        raise CantRateYourArticle

    # check if user has rated an article
    already_exists = article.article_ratings.filter(rated_by__pkid=author.pkid).exists()

    if already_exists:
        raise AlreadyRated
    # user entered 0 rating. Rating choices are 1, 2, 3, 4, 5 not 0.
    elif data["value"] == 0:
        formatted_response = {"detail": "You can't give a zero rating"}
        return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)
    else:
        # rate Article
        rating = Rating.objects.create(
            article=article,
            rated_by=request.user,
            value=data["value"],
            review=data["review"],
        )

        print(
            "\n***************************** In ratings.create_article_rating_view *********************************"
        )
        print(f"rating: {rating.rated_by}")
        print(
            "***************************** In ratings.create_article_rating_view *********************************\n"
        )

        return Response(
            {"success": "Rating has been added"}, status=status.HTTP_201_CREATED
        )
