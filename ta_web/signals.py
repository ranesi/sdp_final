from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile
import django.core.exceptions

# It should be noted that this information (user account extension)
# was gleaned from <simpleisbetterthancomplex.com>


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except django.core.exceptions.ObjectDoesNotExist:
        pass
