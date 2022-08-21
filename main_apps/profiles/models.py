from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from main_apps.common.models import TimeStampedUUIDModel

User = get_user_model()

"""
When Django processes Profile model, it identifies that it has a ManyToManyField on itself, and as a result, 
it doesn’t add a profile_set attribute to the Profile class. 
Instead, the ManyToManyField is assumed to be symmetrical – that is, if I can follow you, then you can follow me.

If you do not want symmetry in many-to-many relationships with self, set symmetrical to False. 
This will force Django to add the descriptor for the reverse relationship, 
allowing ManyToManyField relationships to be non-symmetrical.


Let's say you have two instances of Contact, John and Judy. 
You may decide to make John a contact of Judy. 
Should this action also make Judy a contact of John? If so, symmetrical=True. If not, symmetrical=False
"""


class Profile(TimeStampedUUIDModel):
    class Gender(models.TextChoices):
        MALE = "male", _("male")
        FEMALE = "female", _("female")
        OTHER = "other", _("other")
        UNSELECTED = "unselected", _("unselected")

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = PhoneNumberField(
        verbose_name=_("phone number"), max_length=12, default="+12125552368"
    )
    about_me = models.TextField(
        verbose_name=_("about me"), default="a little intro about me........"
    )
    gender = models.CharField(
        verbose_name=_("gender"),
        choices=Gender.choices,
        default=Gender.UNSELECTED,
        max_length=11,
    )
    country = CountryField(
        verbose_name=_("country"), default="GB", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("city"),
        max_length=180,
        default="Hatfield",
        blank=False,
        null=False,
    )
    profile_photo = models.ImageField(
        verbose_name=_("profile photo"), default="/profile_default.png"
    )
    twitter_handle = models.CharField(
        verbose_name=_("twitter handle"), max_length=20, blank=True
    )
    follows = models.ManyToManyField(
        "self", symmetrical=False, related_name="followed_by", blank=True
    )

    def __str__(self):
        return f"{self.user.username}'s profile"

    def following_list(self):
        return self.follows.all()

    def followers_list(self):
        return self.followed_by.all()

    def follow(self, profile):
        self.follows.add(profile)

    def unfollow(self, profile):
        self.follows.remove(profile)

    def check_following(self, profile):
        return self.follows.filter(pkid=profile.pkid).exists()

    def check_is_followed_by(self, profile):
        return self.followed_by.filter(pkid=profile.pkid).exists()
