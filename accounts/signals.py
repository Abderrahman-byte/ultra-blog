from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from .models import Profil

@receiver(post_save, sender=User)
def create_profil(sender, instance, created, **kwargs) :
    if created :
        Profil.objects.create(
            user=instance,
            username=instance.username,
            email=instance.email
        )

@receiver(post_save, sender=Profil)
def update_profil(sender, instance, created, **kwargs) :
    if not created :
        user = instance.user
        user.email = instance.email
        user.username = instance.username
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.save()