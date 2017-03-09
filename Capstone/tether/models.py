from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# League model, PK is league_id and FK is to User
class League(models.Model):
    # league_id = models.primary_key = True ###Can be default ID or this
    league_name = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    #skill_level = models.CharField(max_length=255)
    #members = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default='', unique=True)

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
############################################################################


#############################################################################
# Expanding the default django User class to add more fields/attributes
# One to one with django default user




class MatchPlayers(models.Model):
    #in_match = models.ForeignKey(DotaData, on_delete=models.CASCADE)
    #in_match = models.ForeignKey(DotaData, on_delete=models.CASCADE, default=1)
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



class NewRecentMatches1(models.Model):
    id_match0 = models.CharField(max_length=200)
    id_match1 = models.CharField(max_length=200)
    id_match2 = models.CharField(max_length=200)
    id_match3 = models.CharField(max_length=200)
    id_match4 = models.CharField(max_length=200)
    players = models.ManyToManyField(MatchPlayers, through='PlayersInMatch')
    # steam_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "new_recent_matches1"
        verbose_name_plural = 'Recent matches'

    # Returns match_id
    def __unicode__(self):
        return self.name



class PlayersInMatch(models.Model):
    match_id = models.ForeignKey(NewRecentMatches1)
    players_id = models.ForeignKey(MatchPlayers)

    class Meta:
        db_table = "players_in_match"
        verbose_name_plural = 'Recent matches'

    # Returns match_id
    def __unicode__(self):
        return self.name

################# OLD PROFILE MODEL, IT WONT LET ME DELETE IT ###########################
#                 Admin.py and forms.py updated for UserProfile1                        #
class UserProfile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=255)
    steam_id = models.IntegerField(unique=True, editable=False, blank=True, null=True)
    win_rate = models.DecimalField(max_digits=10, decimal_places=2, default='0000000000',)
    average_gpm = models.DecimalField(max_digits=6, decimal_places=2, default='000000',)
    league_rank = models.CharField(max_length=255, default='Bronze',)
    #recent_matches = models.ManyToManyField(NewRecentMatches1)

    class Meta:
        db_table = "profile"

    # Returns username instead of unicode
    def __unicode__(self):
        return self.name
################## END OLD PROF MODEL ###################################################

class UserProfile1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.CharField(max_length=255)
    steam_id = models.IntegerField(unique=True, editable=False, blank=True, null=True)
    win_rate = models.DecimalField(max_digits=10, decimal_places=2, default='0000000000',)
    average_gpm = models.DecimalField(max_digits=6, decimal_places=2, default='000000',)
    league_rank = models.CharField(max_length=255, default='Bronze',)
    recent_matches = models.ManyToManyField(NewRecentMatches1, through='Profiles_Matches')

    class Meta:
        db_table = "profile1"

    # Returns username instead of unicode
    def __unicode__(self):
        return self.name

class Profiles_Matches(models.Model):
    profile_id = models.ForeignKey(UserProfile1)
    match_id = models.ForeignKey(NewRecentMatches1)

    class Meta:
        db_table = "profiles_matches"
        verbose_name_plural = 'Recent matches'

    # Returns match_id
    def __unicode__(self):
        return self.name

class MatchData(models.Model):  # data for individual players, NOT overall match
    #player_in_match = models.ForeignKey(MatchPlayers.objects.get(), on_delete=models.CASCADE) #add obj variable to define FK
    backpack_2 = models.IntegerField()
    item_4_name = models.CharField(max_length=200)
    kills = models.IntegerField()
    leaver_status_description = models.CharField(max_length=200)
    item_0_name = models.CharField(max_length=200)
    item_3_name = models.CharField(max_length=200)
    hero_healing = models.IntegerField( default=1,blank=True,null=True)
    gold_per_min = models.IntegerField()
    hero_id = models.IntegerField()
    item_0 = models.IntegerField()
    backpack_0 = models.IntegerField()
    scaled_hero_healing = models.IntegerField(default=1,blank=True,null=True)
    scaled_tower_damage = models.IntegerField(default=1,blank=True,null=True)
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

class CommonData(models.Model):
    # num_match = models.ForeignKey(RecentMatches, to_field='match_id', on_delete=models.CASCADE)
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
    # num_match = models.ForeignKey(RecentMatches, on_delete=models.CASCADE)

    # num_match = models.ForeignKey(RecentMatches, on_delete=models.CASCADE)
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