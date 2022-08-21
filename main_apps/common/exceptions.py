"""
exc: {
      'username': [ErrorDetail(string='This field may not be blank.', code='blank')],
      'first_name': [ErrorDetail(string='This field may not be blank.', code='blank')],
      'last_name': [ErrorDetail(string='This field may not be blank.', code='blank')],
      'email': [ErrorDetail(string='This field may not be blank.', code='blank')],
      'password': [ErrorDetail(string='This field may not be blank.', code='blank')],
      're_password': [ErrorDetail(string='This field may not be blank.', code='blank')]
      }
handlers[exception_class](exc, context, response): <Response status_code=400, "text/html; charset=utf-8">
exception_class: ValidationError
context: {
          'view': <djoser.views.UserViewSet object at 0x7f6b5ec85ee0>,
          'args': (),
          'kwargs': {},
          'request': <rest_framework.request.Request: POST '/api/v1/auth/users/'>
          }

response = {"status_code": 400,
            "errors": {"status_code": 400,
                       "errors": {"username": ["This field is required."],
                                  "first_name": ["This field is required."],
                                  "last_name": ["This field is required."],
                                  "email": ["This field is required."],
                                  "password": ["This field is required."],
                                  "re_password": ["This field is required."]}
                       }
            }
"""
from rest_framework.views import exception_handler


def common_exception_handler(exc, context):
    response = exception_handler(exc, context)

    handlers = {
        "NotFound": _handle_not_found_error,
        "ValidationError": _handle_generic_error,
    }

    # name of the exception class
    exception_class = exc.__class__.__name__

    # if the exception_class can be handled by the custom exception
    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    # return the exception from Django
    return response


def _handle_generic_error(exc, context, response):
    status_code = response.status_code
    # added status_code to response data even though the errors dictionary contains the status_code
    response.data = {"status_code": status_code, "errors": response.data}

    return response


def _handle_not_found_error(exc, context, response):
    view = context.get("view", None)

    if view and hasattr(view, "queryset") and view.queryset is not None:
        status_code = response.status_code
        error_key = view.queryset.model._meta.verbose_name
        response.data = {
            "status_code": status_code,
            "errors": {error_key: response.data["detail"]},
        }

    else:
        response = _handle_generic_error(exc, context, response)
    return response
