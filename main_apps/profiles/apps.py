from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "main_apps.profiles"
    verbose_name = _("Profiles")

    def ready(self):
        # noinspection PyUnresolvedReferences
        from main_apps.profiles import signals
