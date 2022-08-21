import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from api_project.settings.base import AUTH_USER_MODEL
from main_apps.profiles.models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            logger.info(f"user [{instance}] just created")
        except:
            logger.error(
                f"create profile error: could not create user [{instance}'s] profile"
            )


@receiver(post_save, sender=AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
        logger.info(f"updated [{instance}'s] profile")
    except:
        logger.error(
            f"update profile error: error updating user [{instance}'s] profile"
        )
