import django_tables2 as tables
from tether.models import League
from django_tables2.utils import A
from django.db.models import Count

class LeagueTable(tables.Table):
    league_name = tables.Column()
    region = tables.Column()
    skill_level = tables.Column()
    password_status = tables.Column(orderable=False)
    players = tables.Column(orderable=False)
    submit_column = tables.LinkColumn('public_league', verbose_name='Join', args=[A('slug')], empty_values=(), text='View', orderable=False)

    class Meta:
        attrs = {'class': 'table table-bordered table-hover'}
