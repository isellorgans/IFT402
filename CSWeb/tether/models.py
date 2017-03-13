from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver


# League model, PK is league_id and FK is to User
class League(models.Model):
    # league_id = models.primary_key = True ###Can be default ID or this
    league_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    SKILL_LEVELS = (
        ('Bronze', 'Bronze'),
        ('Silver', 'Silver'),
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond'),
    )
    skill_level = models.CharField(max_length=255, default='BZ', blank=True, choices=SKILL_LEVELS)
    #members = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(default='', unique=True)

    def players(self):
        return self.userprofile_set.count() + 1

    def password_status(self):
        if self.password is not '' or None:
            return "Yes"
        else:
            return "No"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.league_name)
        super(League, self).save(*args, **kwargs)

    class Meta:
        db_table = "league"

    # Returns league name
    def __unicode__(self):
        return self.name


class PrizePool(models.Model):
    league_id = models.IntegerField()
    prize_pool = models.IntegerField()
    status = models.IntegerField()

    class Meta:
        db_table = "prize_pool"

    # idk what this does
    # Returns username instead of unicode
    def __unicode__(self):
        return self.name


class RecentMatches(models.Model):
    match_id = models.CharField(max_length=200, primary_key=True)
    match_num = models.CharField(max_length=200)

    # steam_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "recent_matches"
        verbose_name_plural = 'Recent matches'

    # Returns match_id
    def __unicode__(self):
        return self.name


# Expanding the default django User class to add more fields/attributes
# One to one with django default user


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    leagues = models.ManyToManyField(League)
    region = models.CharField(max_length=255)
    steam_id = models.IntegerField(unique=True, editable=False, blank=True, null=True)
    win_rate = models.DecimalField(max_digits=10, decimal_places=2, default='0000000000',)
    average_gpm = models.DecimalField(max_digits=6, decimal_places=2, default='000000',)
    league_rank = models.CharField(max_length=255, default='Bronze',)
    recent_matches = models.ManyToManyField(RecentMatches)

    class Meta:
        db_table = "profile"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    # Returns username instead of unicode
    def __unicode__(self):
        return self.name


class CommonData(models.Model):
    num_match = models.ForeignKey(RecentMatches, default=1)
    lobby_name = models.CharField(max_length=200)
    game_mode = models.CharField(max_length=200)
    match_id = models.CharField(max_length=200)
    human_players = models.IntegerField()
    engine = models.IntegerField()
    game_mode_name = models.CharField(max_length=200)
    duration = models.IntegerField()
    cluster = models.IntegerField()
    start_time = models.IntegerField()
    lobby_type = models.IntegerField()

    class Meta:
        db_table = "common_data"

    # idk what this does
    # Returns username instead of unicode
    def __unicode__(self):
        return self.name


class DotaData(models.Model):
        num_match = models.ForeignKey(RecentMatches, default=1, )
        tower_status_radiant = models.IntegerField()
        radiant_win = models.BooleanField()
        pre_game_duration = models.IntegerField()
        tower_status_dire = models.IntegerField()
        barracks_status_radiant = models.IntegerField()
        flags = models.IntegerField()
        leagueid = models.IntegerField()
        match_id = models.CharField(max_length=200)
        cluster_name = models.CharField(max_length=200)
        positive_votes = models.IntegerField()
        radiant_score = models.IntegerField()
        match_seq_num = models.BigIntegerField()
        barracks_status_dire = models.IntegerField()
        first_blood_time = models.IntegerField()
        dire_score = models.IntegerField()
        negative_votes = models.IntegerField()

        class Meta:
            db_table = "dota_data"

            # Returns username instead of unicode

        def __unicode__(self):
            return self.name


class MatchPlayers(models.Model):
    in_match = models.ForeignKey(DotaData, default=1)
    player0_id = models.BigIntegerField()
    p1ayer3_id = models.BigIntegerField()
    p1ayer1_id = models.BigIntegerField()
    p1ayer4_id = models.BigIntegerField()
    p1ayer2_id = models.BigIntegerField()
    p1ayer7_id = models.BigIntegerField()
    p1ayer8_id = models.BigIntegerField()
    p1ayer9_id = models.BigIntegerField()
    p1ayer6_id = models.BigIntegerField()
    p1ayer5_id = models.BigIntegerField()

    class Meta:
        db_table = "match_players"

    # Returns match_id
    def __unicode__(self):
        return self.name


class MatchData(models.Model):  # data for individual players, NOT overall match
    player_in_match = models.ForeignKey(MatchPlayers, default=1)
    backpack_2 = models.IntegerField()
    item_4_name = models.CharField(max_length=200)
    kills = models.IntegerField()
    leaver_status_description = models.CharField(max_length=200)
    item_0_name = models.CharField(max_length=200)
    item_3_name = models.CharField(max_length=200)
    hero_healing = models.IntegerField()
    gold_per_min = models.IntegerField()
    hero_id = models.IntegerField()
    item_0 = models.IntegerField()
    backpack_0 = models.IntegerField()
    scaled_hero_healing = models.IntegerField()
    scaled_tower_damage = models.IntegerField()
    assists = models.IntegerField()
    item_4 = models.IntegerField()
    tower_damage = models.IntegerField()
    item_1_name = models.CharField(max_length=200)
    xp_per_min = models.IntegerField()
    hero_damage = models.IntegerField()
    item_2_name = models.CharField(max_length=200)
    player_slot = models.IntegerField()
    item_5_name = models.CharField(max_length=200)
    gold = models.IntegerField()
    level = models.IntegerField()
    scaled_hero_damage = models.IntegerField()
    denies = models.IntegerField()
    item_5 = models.IntegerField()
    leaver_status = models.IntegerField()
    item_3 = models.IntegerField()
    last_hits = models.IntegerField()
    item_1 = models.IntegerField()
    item_2 = models.IntegerField()
    gold_spent = models.IntegerField()
    hero_name = models.CharField(max_length=200)
    backpack_1 = models.IntegerField()
    leaver_status_name = models.CharField(max_length=200)
    deaths = models.IntegerField()

    class Meta:
        db_table = "match_data"

    # Returns match_id
    def __unicode__(self):
        return self.name









# *** OLD MODEL BACKUP ***
'''
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
'''