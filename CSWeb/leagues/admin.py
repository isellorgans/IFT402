from django.contrib import admin
from leagues.models import UserProfile, League, RecentMatches


class LeagueAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('league_name',)}


admin.site.register(UserProfile)
admin.site.register(League, LeagueAdmin)
admin.site.register(RecentMatches)
