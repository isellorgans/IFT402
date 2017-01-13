from django.db import models
from django.contrib.auth.models import User


# Expanding the default django User class to add more fields/attributes
# One to one with django default user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=255)

    # steam_id = models.unique = True
    # win_rate = models.DecimalField(max_digits=10, decimal_places=2)
    # average_gpm = models.IntegerField()
    # league_rank = models.CharField(max_length=255)

    # Returns username instead of unicode
    def __unicode__(self):
        return self.user.username

    # League model, PK is league_id and FK is to User
    # class League(models.Model):
    # league_id = models.primary_key = True
    # league_name = models.CharField(max_length=255)
    # region = models.CharField(max_length=255)
    # skill_level = models.CharField(max_length=255)
    # members = models.CharField(max_length=255)
    # l_id = models.ForeignKey(User, on_delete=models.CASCADE)

    # Returns league name
    #def __unicode__(self):
        #return self.league.league_name

    # Recent_Matches model, pk is match_id, FK is to steam_id in User_Profile
    # class RecentMatches(models.Model):
    # match_id = models.primary_key = True
    # skill_level = models.CharField(max_length=255)
    # date = models.DateField()
    # hero_id = models.IntegerField()
    # result_wl = models.BooleanField()
    # kda = models.FloatField()
    # gpm = models.FloatField()
    # steam_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    # Returns match_id
    #def __unicode__(self):
        #return self.league.match_id
