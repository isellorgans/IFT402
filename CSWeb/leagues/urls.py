from django.conf.urls import url
from leagues import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^publicleague/(?P<league_name_slug>[\w\-]+)/$', views.public_leagues, name='public_league')
]
