from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Profile(models.Model):
    """
    profile class for user model.
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(null=True,blank=True)
    age = models.PositiveSmallIntegerField(null=True,blank=True)
    phone = models.PositiveSmallIntegerField(null=True, blank=True)


def save_profile(sender, **kwargs):
    """
    receives signal from user model when an instance of user
    has been created.
    then it creates a profile for that user model.
    """
    if kwargs['created']:
        profile = Profile(user=kwargs['instance'])
        profile.save()

post_save.connect(receiver=save_profile, sender=User)