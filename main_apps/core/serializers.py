from django.contrib.auth import get_user_model
from django_countries.serializer_fields import CountryField
from djoser.serializers import UserCreateSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

User = get_user_model()


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "password"]


class UserSerializer(serializers.ModelSerializer):
    # source: ref the 'gender' field in profile using the related_name="profile" for the OneToOneField in profiles app
    gender = serializers.CharField(source="profile.gender")
    phone_number = PhoneNumberField(source="profile.phone_number")
    profile_photo = serializers.ReadOnlyField(source="profile.profile_photo")
    country = CountryField(source="profile.country")
    city = serializers.CharField(source="profile.city")
    # SerializerMethodField: binds the function get_first_name to this field. i.e. get_{field_name}
    first_name = serializers.SerializerMethodField()
    # SerializerMethodField: binds the function get_first_name to this field. i.e. get_{field_name}
    last_name = serializers.SerializerMethodField()
    # SerializerMethodField: binds the function get_first_name to this field. i.e. get_{field_name}
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "gender",
            "phone_number",
            "profile_photo",
            "country",
            "city",
        ]

    def get_first_name(self, obj):
        """
        Used for the SerializerMethodField for first_name
        obj: reps the User model
        """
        print(
            "\n----------------------------------- In get_first_name -------------------------------------"
        )
        print(f"obj: {obj}")
        print(
            "----------------------------------- In get_first_name -------------------------------------\n"
        )
        return obj.first_name.title()

    def get_last_name(self, obj):
        """
        Used for the SerializerMethodField for last_name
        obj: reps the User model
        """
        print(
            "\n----------------------------------- In get_last_name -------------------------------------"
        )
        print(f"obj: {obj}")
        print(
            "----------------------------------- In get_last_name -------------------------------------\n"
        )
        return obj.last_name.title()

    def get_full_name(self, obj):
        """
        Used for the SerializerMethodField for full_name
        obj: reps the User model
        """
        print(
            "\n----------------------------------- In get_full_name -------------------------------------"
        )
        print(f"obj: {obj}")
        print(
            "----------------------------------- In get_full_name -------------------------------------\n"
        )
        first_name = obj.user.first_name.title()
        last_name = obj.user.last_name.title()
        return f"{first_name} {last_name}"

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation
