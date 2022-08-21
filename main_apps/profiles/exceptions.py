from rest_framework.exceptions import APIException


class NotYourProfile(APIException):
    status_code = 403
    default_detail = "Cannot Edit: This profile doesn't belong to you!"


class CannotFollowYourself(APIException):
    status_code = 403
    default_detail = "You cannot follow yourself!"
