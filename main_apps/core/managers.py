from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        """checks if the email is valid using the 'validate_email' function"""
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Email is invalid"))

    def create_user(
        self, username, first_name, last_name, email, password, **extra_fields
    ):
        if not username:
            raise ValueError(_("Username must be provided"))

        if not first_name:
            raise ValueError(_("First name must be provided"))

        if not last_name:
            raise ValueError(_("Last name must be provided"))

        if email:
            # Normalize the email address by lower-casing the domain part of it i.e. makes the second part of the email
            # address case-insensitive. For email addresses, foo@bar.com and foo@BAR.com are equivalent
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Email address must be provided"))

        # create user instance
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )

        # encrypt password
        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        # for supporting multiple databases
        user.save(using=self._db)
        return user

    def create_superuser(
        self, username, first_name, last_name, email, password, **extra_fields
    ):
        """create a superuser(Admin)"""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must be a staff"))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must set to True"))

        if not password:
            raise ValueError(_("Superusers must have a password"))

        if email:
            # Normalize the email address by lower-casing the domain part of it i.e. makes the second part of the email
            # address case-insensitive. For email addresses, foo@bar.com and foo@BAR.com are equivalent
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Email address must be provided for an Admin"))

        # create user instance
        user = self.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            **extra_fields
        )
        # for supporting multiple databases
        user.save(using=self._db)
        return user
