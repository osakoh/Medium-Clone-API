# from multiprocessing import context
# from unicodedata import name

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from api_project.settings.production import DEFAULT_FROM_EMAIL

from .exceptions import CannotFollowYourself, NotYourProfile
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer

User = get_user_model()


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    renderer_classes = (ProfilesJSONRenderer,)
    pagination_class = ProfilePagination


class ProfileDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    # optimize qs: OneToOne relationship btw Profile & User
    # In Profile model: user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # Not-optimized: Profile.objects.get(user__username=username)
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def retrieve(self, request, username, *args, **kwargs):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        serializer = self.serializer_class(profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # optimize qs: OneToOne relationship btw Profile & User
    # In Profile model: user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # Not-optimized: Profile.objects.get(user__username=username)
    queryset = Profile.objects.select_related("user")
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request, username):
        try:
            self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        user_name = request.user.username
        if user_name != username:
            # custom Profile exception
            raise NotYourProfile

        data = request.data
        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_my_followers(request, username):
    """
    :param request: what the client's send to the server
    :param username: the username to get all followers
    :return: returns all followers of a specific user through the username
    """
    try:
        specific_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound("User with that username does not exist")

    user_profile_instance = Profile.objects.get(user__pkid=specific_user.pkid)

    # using the reverse relationship between the User & Profile model
    user_followers = user_profile_instance.following_list()
    serializer = FollowingSerializer(user_followers, many=True)

    response = {
        "status_code": status.HTTP_200_OK,
        "followers": serializer.data,
        "num_of_followers": len(serializer.data),
    }

    return Response(response, status=status.HTTP_200_OK)


class FollowUnfollowAPIView(generics.GenericAPIView):
    """
    View to allow users follow and unfollow each other
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer

    def get(self, request, username):
        """
        returns the status_code, an array of all users a specific user follows and the total number of users in that array
        """
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        user_profile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        my_following_list = user_profile_instance.following_list()
        serializer = ProfileSerializer(my_following_list, many=True)

        response = {
            "status_code": status.HTTP_200_OK,
            "my_followers": serializer.data,
            "num_my_followers": len(serializer.data),
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request, username):
        """
        allows a user to follow another user
        """
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        if specific_user.pkid == request.user.pkid:
            raise CannotFollowYourself

        user_profile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        # check if a user already follows another user
        if current_user_profile.check_following(user_profile_instance):
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You already follow {specific_user.username}",
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        # add the new user to users list/array
        current_user_profile.follow(user_profile_instance)

        # send email notification
        subject = "New follower on Share Gist"
        message = f"Hi {specific_user.username.title()}, {current_user_profile.user.username.title()} now follows you."
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [specific_user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        return Response(
            {
                "status_code": status.HTTP_200_OK,
                "detail": f"You now follow {specific_user.username}",
            }
        )

    def delete(self, request, username):
        """
        unfollows/deletes a specific user from another user's followers list
        """
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        user_profile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        # for a user to be unfollowed, I must first be following that user
        if not current_user_profile.check_following(user_profile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You do not follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        # remove user from array/list
        current_user_profile.unfollow(user_profile_instance)

        response = {
            "status_code": status.HTTP_200_OK,
            "detail": f"You have unfollowed {specific_user.username}",
        }
        return Response(response, status=status.HTTP_200_OK)


"""
@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_all_profiles(request):
    profiles = Profile.objects.all()
    serializer = ProfileSerializer(profiles, many=True)
    response = {"profiles": serializer.data}
    return Response(response, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def get_profile_details(request, username):
    try:
        user_profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        raise NotFound('A profile with this username does not exist...')

    serializer = ProfileSerializer(user_profile, many=False)
    response = {"profile": serializer.data}
    return Response(response, status=status.HTTP_200_OK)
"""
