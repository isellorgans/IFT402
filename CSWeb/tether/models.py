from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Expanding the default django User class to add more fields/attributes
# One to one with django default user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=255)
    steam_id = models.IntegerField(unique=True, editable=False, blank=True, null=True)
    win_rate = models.DecimalField(max_digits=10, decimal_places=2, default='0000000000',)
    average_gpm = models.DecimalField(max_digits=6, decimal_places=2, default='000000',)
    league_rank = models.CharField(max_length=255, default='Bronze',)

    class Meta:
        db_table = "profile"

    # Returns username instead of unicode
    def __unicode__(self):
        return self.name


# League model, PK is league_id and FK is to User
class League(models.Model):
    # league_id = models.primary_key = True ###Can be default ID or this
    league_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    skill_level = models.CharField(max_length=255)
    members = models.CharField(max_length=255)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default='', unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.league_name)
        super(League, self).save(*args, **kwargs)

    class Meta:
        db_table = "league"

    # Returns league name
    def __unicode__(self):
        return self.name


# Recent_Matches model, pk is match_id, FK is to steam_id in User_Profile
class RecentMatches(models.Model):
    # match_id = models.primary_key = True ###Again, can be default id or this
    skill_level = models.CharField(max_length=255)
    date = models.DateField()
    hero_id = models.IntegerField()
    result_wl = models.BooleanField()
    kda = models.FloatField()
    gpm = models.FloatField()
    steam_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "recent_matches"
        verbose_name_plural = 'Recent matches'

    # Returns match_id
    def __unicode__(self):
        return self.name
