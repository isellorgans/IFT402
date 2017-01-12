from django.db import models
from django.contrib.auth.models import User


# Expanding the default django User class to add more fields/attributes
class UserProfile(models.Model):
    user = models.OneToOneField(User)  # , on_delete=models.CASCADE
    country = models.CharField(max_length=20)
    state = models.CharField(max_length=2)

    # Returns username instead of unicode
    def __unicode__(self):
        return self.user.username
