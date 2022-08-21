import re
import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    # pseudo primary key
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(
        max_length=225, verbose_name=_("username"), db_index=True, unique=True
    )
    first_name = models.CharField(max_length=50, verbose_name=_("first name"))
    last_name = models.CharField(max_length=50, verbose_name=_("last name"))
    email = models.EmailField(
        verbose_name=_("email address"),
        db_index=True,
        unique=True,
        help_text=_("Enter email address"),
        error_messages={
            "unique": _("A user is already registered with this email address"),
        },
    )
    is_staff = models.BooleanField(
        verbose_name=_("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        verbose_name=_("active"),
        default=True,
        help_text=(
            _(
                "Designates whether this user should be treated as active. "
                "Unselect this instead of deleting accounts."
            )
        ),
    )
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.username

    # convert username to lowercase before saving
    def save(self, *args, **kwargs):
        """
        returns a lowercase username
        """
        if self.username:
            # remove all spaces/comma/punctuations
            self.username = "".join(re.findall(r"\w", self.username.lower()))
        super(User, self).save(*args, **kwargs)

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def get_short_name(self):
        return self.first_name
