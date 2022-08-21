from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    # source: ref the 'username' field in user using the related_name="profile" for the OneToOneField in profiles app
    # i.e. user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = serializers.CharField(source="user.username")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    # SerializerMethodField: binds the function get_full_name to this field. i.e. get_{field_name}
    full_name = serializers.SerializerMethodField(read_only=True)
    profile_photo = serializers.SerializerMethodField()
    country = CountryField(name_only=True)
    # SerializerMethodField: binds the function get_following to this field. i.e. get_{field_name}
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "about_me",
            "phone_number",
            "profile_photo",
            "country",
            "city",
            "twitter_handle",
            "following",
        ]

    def get_full_name(self, obj):
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def get_profile_photo(self, obj):
        return obj.profile_photo.url

    def get_following(self, instance):
        request = self.context.get("request", None)
        if request is None:
            return None
        if request.user.is_anonymous:
            return False

        current_user_profile = request.user.profile
        followee = instance
        following_status = current_user_profile.check_following(followee)

        return following_status


class UpdateProfileSerializer(serializers.ModelSerializer):
    country = CountryField(name_only=True)

    class Meta:
        model = Profile
        fields = [
            "phone_number",
            "profile_photo",
            "about_me",
            "gender",
            "country",
            "city",
            "twitter_handle",
        ]


class FollowingSerializer(serializers.ModelSerializer):
    # source: ref the 'username' field in user using the related_name="profile" for the OneToOneField in profiles app
    # i.e. user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    following = serializers.BooleanField(default=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "first_name",
            "last_name",
            "profile_photo",
            "about_me",
            "twitter_handle",
            "following",
        ]
