from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    message = (
        "You are not allowed to update or delete an article that does not belong to you"
    )

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # allows GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        print(
            "\n******************************* In articles.permissions ****************************************"
        )
        print(f"request: {request}")
        print(f"view: {view}")
        print(f"obj: {obj}")
        print(f"request.method: {request.method}")
        print(f"permissions.SAFE_METHODS: {permissions.SAFE_METHODS}")
        print(f"obj.author: {obj.author}")
        print(f"request.user: {request.user}")
        print(f"obj.__class__.__name__ : {obj.__class__.__name__}")
        print(f"request.auth: {request.auth}")
        print(
            "******************************* In articles.permissions ****************************************\n"
        )

        # Instance must have an attribute named `author`
        return obj.author == request.user
