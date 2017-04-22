import django_tables2 as tables
from tether import models
from tether.models import League
from django_tables2.utils import A
from django.db.models import Count

class LeagueTable(tables.Table):
    league_name = tables.Column()
    region = tables.Column()
    skill_level = tables.Column()
    password_status = tables.Column()
    players = tables.Column()
    submit_column = tables.LinkColumn('public_league', verbose_name='Join', args=[A('slug')], empty_values=(), text='View', orderable=False)

    class Meta:
        attrs = {'class': 'table table-bordered table-hover'}

class ResultsTable(tables.Table):
    league_name = tables.Column(attrs={'tr': {'bgcolor': 'black'}})
    region = tables.Column()
    skill_level = tables.Column()
    password_status = tables.Column()
    players = tables.Column()
    submit_column = tables.LinkColumn('public_league', verbose_name='Join', args=[A('slug')], empty_values=(), text='View', orderable=False)

    class Meta:
        attrs = {'class': 'table table-bordered table-hover'}

class MatchesTable(tables.Table):
    name = tables.Column()
    player1 = tables.Column()
    player2 = tables.Column()
    player3 = tables.Column()
    player4 = tables.Column()
    player5 = tables.Column()
    player6 = tables.Column()
    player7 = tables.Column()
    player8 = tables.Column()
    player9 = tables.Column()
    player10 = tables.Column()
    winner = tables.Column()

    class Meta:
        attrs = {'class': 'table table-bordered table-hover'}

class MatchTable(tables.Table):
    class Meta:
        model = models.NewRecentMatches1
        attrs = {'class': 'table table-bordered table-hover'}


class PlayerTable(tables.Table):
    class Meta:
        model = models.MatchPlayers
        attrs = {'class': 'table table-bordered table-hover'}

class PlayerData(tables.Table):
    class Meta:
        model = models.MatchData
        attrs = {'class': 'table table-bordered table-hover'}