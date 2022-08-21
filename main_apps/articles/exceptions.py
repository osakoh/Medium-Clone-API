from rest_framework.exceptions import APIException


class UpdateArticle(APIException):
    status_code = 403
    default_detail = "This a article does not belong to you'"
