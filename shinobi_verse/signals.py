from django.db.models.signals import post_save
from shinobi_verse.models import CustomUser
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()