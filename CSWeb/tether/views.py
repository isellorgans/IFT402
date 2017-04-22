from tether.forms import UserForm, UserProfileForm, LeagueForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user, logout
from tether.models import League, UserProfile1, Matches, LeagueMembership
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from nested_lookup import nested_lookup
from django.contrib import messages
from django.db.models import Count, F
import dota2api
from django_tables2 import RequestConfig
from tether.tables import LeagueTable, ResultsTable, MatchesTable
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.shortcuts import render
import tether.models
import tether.tables
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist


# from django.urls import NoReverseMatch


def index(request):
    context = dict()

    try:
        l = League.objects.annotate(user_count=Count('userprofile1')).order_by('-user_count')[:5]

        context['leaguename0'] = l[0].league_name
        context['leagueregion0'] = l[0].region
        context['leagueplayers0'] = l[0].players
        context['leagueslug0'] = l[0].slug

        context['leaguename1'] = l[1].league_name
        context['leagueregion1'] = l[1].region
        context['leagueplayers1'] = l[1].players
        context['leagueslug1'] = l[1].slug

        context['leaguename2'] = l[2].league_name
        context['leagueregion2'] = l[2].region
        context['leagueplayers2'] = l[2].players
        context['leagueslug2'] = l[2].slug

        context['leaguename3'] = l[3].league_name
        context['leagueregion3'] = l[3].region
        context['leagueplayers3'] = l[3].players
        context['leagueslug3'] = l[3].slug

        context['leaguename4'] = l[4].league_name
        context['leagueregion4'] = l[4].region
        context['leagueplayers4'] = l[4].players
        context['leagueslug4'] = l[4].slug

    except IndexError:
        l = 'null'

    return render(request, "tether/index.html", context)


def register(request):
    # Initiating boolean for successful registration.
    registered = False

    # Grabbing the form data from the user
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Saving information to the database if reg is valid
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            # Saving userprofile information
            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            # Updating for successful registration
            registered = True

        # Print any errors
        else:
            print(user_form.errors, profile_form.errors)

    # If not a POST request, render the forms blank
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Returning the form depending on context
    return render(request, "tether/register.html",
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    # If its a POST request, gather info from user
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Use django to authenticate user, returns user object on success
        user = authenticate(username=username, password=password)

        # If django retrieved the object, user credentials were correct
        if user:
            # If user is active, log them in and redirect to home
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/tether/index')
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Your username or password was incorrect.")

    return redirect('index')


def user_logout(request):
    logout(request)
    return redirect('index')


def public_leagues(request, league_name_slug):
    context_dict = {'matchbool': False, 'join': True}

    league = League.objects.get(slug=league_name_slug)
    context_dict['league'] = league

    users = league.leaguemembership_set.all()
    context_dict['users'] = users

    matches = league.matches_set.filter(finished=False)
    context_dict['matches'] = matches
    if context_dict['matches'] is not None:
        context_dict['matchbool'] = True

    try:
        user = User.objects.get(pk=request.user.id)
        if user.userprofile1.leagues.filter(league_name=league.league_name):
            context_dict['join'] = False
    except ObjectDoesNotExist:
        user = None
        context_dict['join'] = False

    if league.password_status == 'Yes':
        context_dict['password'] = True

    if league.owner == user:
        context_dict['owner'] = True

    if request.method == 'POST':
        if 'join' in request.POST:
            if league.password_status == "Yes":
                if request.POST.get('password') == league.password:
                    uprofile = user.userprofile1
                    lm = LeagueMembership(league=league, profile=uprofile, player_skill='500')
                    lm.save()
                    user.userprofile1.save()
                    league.save()
                    return HttpResponseRedirect('.')
                else:
                    print("The password was incorrect.")
            else:
                uprofile = user.userprofile1
                lm = LeagueMembership(league=league, profile=uprofile, player_skill='500')
                lm.save()
                user.userprofile1.save()
                league.save()
                return HttpResponseRedirect('.')
        elif 'make' in request.POST:
            m = request.POST.get('makefield')
            Matches.objects.create(lobby=league, name=m)
            return HttpResponseRedirect('.')
        elif 'kick' in request.POST:
            if league.owner == user:
                kp = request.POST.get('kick')
                print(kp)
                league.leaguemembership_set.filter(profile_id=kp).delete()
                league.save()
                return HttpResponseRedirect('.')
        elif 'delete' in request.POST:
            if league.owner == user:
                dl = request.POST.get('delete')
                print(dl)
                league.matches_set.filter(id=dl).delete()
                league.save()
                return HttpResponseRedirect('.')

    table = MatchesTable(Matches.objects.filter(lobby=league.id))
    context_dict['table'] = table

    return render(request, 'tether/public_leagues.html', context_dict)


def matches(request, match_id):
    context_dict = {}
    match = Matches.objects.get(id=match_id)
    context_dict['match'] = match
    league = League.objects.get(matches=match)
    try:
        user = User.objects.get(pk=request.user.id)
    except ObjectDoesNotExist:
        user = None
    if league.owner == user:
        context_dict['owner'] = True

    #if user.userprofile1.leagues.get(league_name=league.league_name).DoesNotExist:
        #return HttpResponse("You are not a part of this league.")

    if request.method == 'POST':
        if not match.locked:
            if 'p1' in request.POST:
                p = request.user.username
                if match.player2 == p:
                    match.player2 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player9 == p:
                    match.player9 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player1 = p
                match.save()
            elif 'p2' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player9 == p:
                    match.player9 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player2 = p
                match.save()
            elif 'p3' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player2 == p:
                    match.player2 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player9 == p:
                    match.player9 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player3 = p
                match.save()
            elif 'p4' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player2 == p:
                    match.player2 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player9 == p:
                    match.player9 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player4 = p
                match.save()
            elif 'p5' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player2 == p:
                    match.player2 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player9 == p:
                    match.player9 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player5 = p
                match.save()
            elif 'p6' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player2 == p:
                    match.player2 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player9 == p:
                    match.player9 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player6 = p
                match.save()
            elif 'p7' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player2 == p:
                    match.player2 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player9 == p:
                    match.player9 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player7 = p
                match.save()
            elif 'p8' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player2 == p:
                    match.player2 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player9 == p:
                    match.player9 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player8 = p
                match.save()
            elif 'p9' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player2 == p:
                    match.player2 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player10 == p:
                    match.player10 = ''
                match.player9 = p
                match.save()
            elif 'p10' in request.POST:
                p = request.user.username
                if match.player1 == p:
                    match.player1 = ''
                if match.player2 == p:
                    match.player2 = ''
                if match.player3 == p:
                    match.player3 = ''
                if match.player4 == p:
                    match.player4 = ''
                if match.player5 == p:
                    match.player5 = ''
                if match.player6 == p:
                    match.player6 = ''
                if match.player7 == p:
                    match.player7 = ''
                if match.player8 == p:
                    match.player8 = ''
                if match.player9 == p:
                    match.player9 = ''
                match.player10 = p
                match.save()
            elif 'start' in request.POST:
                match.locked = True
                match.save()
                return HttpResponseRedirect('.')
        elif 'team1' in request.POST and not match.finished:
            if match.player1 is not '':
                p1id = User.objects.get(username=match.player1).userprofile1.id
                p1 = LeagueMembership.objects.get(profile=p1id, league=league.id)
                p1.player_skill = F('player_skill') + 15
                p1.save()
            if match.player2 is not '':
                p2id = User.objects.get(username=match.player2).userprofile1.id
                p2 = LeagueMembership.objects.get(profile=p2id, league=league.id)
                p2.player_skill = F('player_skill') + 15
                p2.save()
            if match.player3 is not '':
                p3id = User.objects.get(username=match.player3).userprofile1.id
                p3 = LeagueMembership.objects.get(profile=p3id, league=league.id)
                p3.player_skill = F('player_skill') + 15
                p3.save()
            if match.player4 is not '':
                p4id = User.objects.get(username=match.player4).userprofile1.id
                p4 = LeagueMembership.objects.get(profile=p4id, league=league.id)
                p4.player_skill = F('player_skill') + 15
                p4.save()
            if match.player5 is not '':
                p5id = User.objects.get(username=match.player5).userprofile1.id
                p5 = LeagueMembership.objects.get(profile=p5id, league=league.id)
                p5.player_skill = F('player_skill') + 15
                p5.save()
            if match.player6 is not '':
                p6id = User.objects.get(username=match.player6).userprofile1.id
                p6 = LeagueMembership.objects.get(profile=p6id, league=league.id)
                p6.player_skill = F('player_skill') - 15
                p6.save()
            if match.player7 is not '':
                p7id = User.objects.get(username=match.player7).userprofile1.id
                p7 = LeagueMembership.objects.get(profile=p7id, league=league.id)
                p7.player_skill = F('player_skill') - 15
                p7.save()
            if match.player8 is not '':
                p8id = User.objects.get(username=match.player8).userprofile1.id
                p8 = LeagueMembership.objects.get(profile=p8id, league=league.id)
                p8.player_skill = F('player_skill') - 15
                p8.save()
            if match.player9 is not '':
                p9id = User.objects.get(username=match.player9).userprofile1.id
                p9 = LeagueMembership.objects.get(profile=p9id, league=league.id)
                p9.player_skill = F('player_skill') - 15
                p9.save()
            if match.player10 is not '':
                p10id = User.objects.get(username=match.player10).userprofile1.id
                p10 = LeagueMembership.objects.get(profile=p10id, league=league.id)
                p10.player_skill = F('player_skill') - 15
                p10.save()

            match.finished = True
            match.winner = 'Team 1'
            match.save()
            return HttpResponseRedirect('.')

        elif 'team2' in request.POST and not match.finished:
            if match.player1 is not '':
                p1id = User.objects.get(username=match.player1).userprofile1.id
                p1 = LeagueMembership.objects.get(profile=p1id, league=league.id)
                p1.player_skill = F('player_skill') - 15
                p1.save()
            if match.player2 is not '':
                p2id = User.objects.get(username=match.player2).userprofile1.id
                p2 = LeagueMembership.objects.get(profile=p2id, league=league.id)
                p2.player_skill = F('player_skill') - 15
                p2.save()
            if match.player3 is not '':
                p3id = User.objects.get(username=match.player3).userprofile1.id
                p3 = LeagueMembership.objects.get(profile=p3id, league=league.id)
                p3.player_skill = F('player_skill') - 15
                p3.save()
            if match.player4 is not '':
                p4id = User.objects.get(username=match.player4).userprofile1.id
                p4 = LeagueMembership.objects.get(profile=p4id, league=league.id)
                p4.player_skill = F('player_skill') - 15
                p4.save()
            if match.player5 is not '':
                p5id = User.objects.get(username=match.player5).userprofile1.id
                p5 = LeagueMembership.objects.get(profile=p5id, league=league.id)
                p5.player_skill = F('player_skill') - 15
                p5.save()
            if match.player6 is not '':
                p6id = User.objects.get(username=match.player6).userprofile1.id
                p6 = LeagueMembership.objects.get(profile=p6id, league=league.id)
                p6.player_skill = F('player_skill') + 15
                p6.save()
            if match.player7 is not '':
                p7id = User.objects.get(username=match.player7).userprofile1.id
                p7 = LeagueMembership.objects.get(profile=p7id, league=league.id)
                p7.player_skill = F('player_skill') + 15
                p7.save()
            if match.player8 is not '':
                p8id = User.objects.get(username=match.player8).userprofile1.id
                p8 = LeagueMembership.objects.get(profile=p8id, league=league.id)
                p8.player_skill = F('player_skill') + 15
                p8.save()
            if match.player9 is not '':
                p9id = User.objects.get(username=match.player9).userprofile1.id
                p9 = LeagueMembership.objects.get(profile=p9id, league=league.id)
                p9.player_skill = F('player_skill') + 15
                p9.save()
            if match.player10 is not '':
                p10id = User.objects.get(username=match.player10).userprofile1.id
                p10 = LeagueMembership.objects.get(profile=p10id, league=league.id)
                p10.player_skill = F('player_skill') + 15
                p10.save()

            match.finished = True
            match.winner = 'Team 2'
            match.save()
            return HttpResponseRedirect('.')

    return render(request, 'tether/matches.html', context_dict)


def join_public(request):  # view for users to look for leagues
    results = None  # initiating results
    if request.method == 'GET':  # if its a get request
        search_query = request.GET.get('search_box', None)  # get the query entered into the search box
        if search_query is not None:
            results = ResultsTable(League.objects.filter(  # django query to get any league object that
                Q(league_name__icontains=search_query) |  # contains the user's query and put into
                Q(region__icontains=search_query) |  # a results table
                Q(skill_level__icontains=search_query) |
                Q(password_status__icontains=search_query) |
                Q(players__icontains=search_query)
            ))

    table = LeagueTable(League.objects.all())  # if there was no search query, generate normal table
    RequestConfig(request, paginate={'per_page': 20}).configure(table)  # paginate table

    return render(request, "tether/join_public.html", {'table': table, 'results': results})
    # return the template with provided context, ie. with users searched leagues.


@login_required(login_url='/tether/login/')  # login decorator that requires login if user is not
def add_league(request):  # view for users to create leagues
    if request.method == 'POST':  # if it a post request
        form = LeagueForm(request.POST)  # give the django form the user's input
        user = User.objects.get(pk=request.user.id)  # identify user

        if form.is_valid():
            forminstance = form.save(commit=False)  # associate user input but don't push to DB yet
            forminstance.owner = user  # label the user as owner of the league
            forminstance.save()  # save to database
            league = League.objects.filter(owner=user).latest('id')  # query to get the just saved league
            uprofile = user.userprofile1
            lm = LeagueMembership(league=league, profile=uprofile, player_skill='500')
            lm.save()  # create and save an association with the user and the league
            league.save()
            return index(request)
        else:
            print(form.errors)  # print errors if form is not valid
    else:
        form = LeagueForm()  # provide the form if user hasn't posted yet

    return render(request, 'tether/create.html', {'form': form})  # return with form context


@login_required(login_url='/tether/login/')
def profile(request):
    if request.user.is_authenticated():
        userr = request.user.username
        sid = request.user.userprofile1.steam_id
        # mid = request.user.userprofile1.profiles_matches_set.all()

        # mid = tether.models.NewRecentMatches1.objects.filter(userprofile1__user=request.user)
        # mat_id = tether.models.NewRecentMatches1.objects.filter(
        # mat_id = request.user.userprofile1.recent_matches.values('id_match4').distinct()




        api = dota2api.Initialise("BFF23F667B3B31FD01663D230DF11C25")

        # -----------------------------------------------------------------------------------------------
        # --- New recent matches attempt ---#

        class History():

            '''
            def get_profile_match_hist(self):
                api = dota2api.Initialise("BFF23F667B3B31FD01663D230DF11C25")
                hist = api.get_match_history(account_id=tether.models.UserProfile.objects.values('steam_id'))  # steam id queryset
                match_list2 = hist

                # nested_lookup('match_id', recent_matches)
                ids = nested_lookup('match_id', match_list2)  # return in list all ids and dates
                s_time = nested_lookup('start_time', match_list2)

                match_list = dict(zip(s_time, ids))  # zip ids and dates into dict
                num_ids = range(4)
                num_matches2 = range(5)
                match_incre2 = []

                for i in num_matches2:
                    match_incre2.append('id_match' + str(i))
                match_ids = ids[:5]
                recent_matches2 = dict(zip(match_incre2, match_ids))


                matches = {str(k): str(v) for k, v in recent_matches2.items()}

                print(matches)
                new_entry = tether.models.NewRecentMatches1(**matches)
                new_entry.save()
            #get_profile_match_hist()
            #--- end ---#
            '''

        class PlayersAndData(History):

            # get_match_players()
            # ----- Save match details / separate players and player details to sep table -----#
            def get_profile_match_hist(self):
                sid = request.user.userprofile1.steam_id
                api = dota2api.Initialise("BFF23F667B3B31FD01663D230DF11C25")
                # hist = api.get_match_history(account_id=tether.models.UserProfile1.objects.values('steam_id'))  # steam id queryset

                # getsid()
                # hist = api.get_match_history(account_id=views.getsid())

                # test = tether.views.profile.sid
                hist = api.get_match_history(account_id=sid)

                match_list2 = hist

                # nested_lookup('match_id', recent_matches)
                ids = nested_lookup('match_id', match_list2)  # return in list all ids and dates
                s_time = nested_lookup('start_time', match_list2)

                match_list = dict(zip(s_time, ids))  # zip ids and dates into dict
                num_ids = range(4)
                num_matches2 = range(5)
                match_incre2 = []

                for i in num_matches2:
                    match_incre2.append('id_match' + str(i))
                match_ids = ids[:5]
                recent_matches2 = dict(zip(match_incre2, match_ids))

                matches = {str(k): str(v) for k, v in recent_matches2.items()}

                print(matches)
                new_entry = tether.models.NewRecentMatches1(**matches)
                # new_entry = p_entry.players.create(tether.models.NewRecentMatches(**matches))
                new_entry.save()

                prof_id = tether.models.UserProfile1.objects.get(steam_id=sid)
                prof_id.save()
                prof = tether.models.Profiles_Matches(profile_id=prof_id, match_id=new_entry)
                prof.save()
                plrs = self.get_match_players()

                PIM = tether.models.PlayersInMatch(players_id=plrs, match_id=new_entry)
                PIM.save()

            # --- end ---#
            # ----- Set up for match players -----#




            def get_match_players(self):
                api = dota2api.Initialise("BFF23F667B3B31FD01663D230DF11C25")
                # test------

                mid = tether.models.NewRecentMatches1.objects.values('id_match4').distinct()
                mat_id = tether.models.NewRecentMatches1.objects.filter(userprofile1__steam_id=sid).values_list(
                    'id_match4').distinct()

                print(mid)
                print(mat_id)

                a = mat_id
                mat_id = " ".join([x[0] for x in a])
                print(mat_id)

                # end test-----
                match_ini = api.get_match_details(match_id=mat_id)  # tether.models.NewRecentMatches1.objects.filter())
                ini2 = api.get_match_details(
                    match_id=mat_id)  # tether.models.NewRecentMatches.objects.values.id_match0(3037647418))
                # hist = api.get_match_history(account_id=tether.models.UserProfile1.objects.values('steam_id')) # steam id queryset
                hist = api.get_match_history(account_id=sid)
                # hist = api.get_match_history(account_id=tether.views.profile.sid) # steam id queryset
                # ----- remove extraneous data -----#
                if 'picks_bans' in match_ini:
                    del match_ini['picks_bans']
                    del ini2['picks_bans']

                if 'ability_upgrades' in hist:
                    del match_ini['ability_upgrades']
                    del ini2['ability_upgrades']

                if 'ability_upgrades' in match_ini:
                    del match_ini['ability_upgrades']
                    del ini2['ability_upgrades']
                # ----- end remove -----#

                self.match_plrs = {}
                self.match_plrs = match_ini.pop("players")

                match_plrs_id = {}
                temp = {}

                # ----- End set up -----#

                # *****CONVERT TO LOOP
                temp = self.match_plrs[0]
                temp = temp.pop("account_id")
                match_plrs_id['player0_id'] = temp

                temp = self.match_plrs[1]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer1_id'] = temp

                temp = self.match_plrs[2]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer2_id'] = temp

                temp = self.match_plrs[3]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer3_id'] = temp

                temp = self.match_plrs[4]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer4_id'] = temp

                temp = self.match_plrs[5]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer5_id'] = temp

                temp = self.match_plrs[6]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer6_id'] = temp

                temp = self.match_plrs[7]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer7_id'] = temp

                temp = self.match_plrs[8]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer8_id'] = temp

                temp = self.match_plrs[9]
                temp = temp.pop("account_id")
                match_plrs_id['p1ayer9_id'] = temp

                # *************** END "LOOP" *******************************

                p_entry = tether.models.MatchPlayers(**match_plrs_id)
                p_entry.save()

                # p_entry.players.add(self.new_entry)
                # return self.match_plrs
                return p_entry

            def get_all_data(self):
                plrs_match_data = {}

                for account_id in self.match_plrs:
                    if account_id in self.match_plrs and self.match_plrs != 0:
                        plrs_match_data = self.match_plrs[
                            1]  # grabs the account id from the player data at the top of the stack
                        del self.match_plrs[1]  # define function to loop through all players,

                        ### CONNECT FORM VALUE (0-9) HERE ^^^^ ###

                if 'ability_upgrades' in plrs_match_data:
                    del plrs_match_data['ability_upgrades']
                print(self.match_plrs)
                print(plrs_match_data)
                match_data_entry = tether.models.MatchData(**plrs_match_data)
                match_data_entry.save()

                # ----- End match details -----#
                # get_all_data()


                # ----- Split common GD -----#

            def get_common_d(self):

                mid = tether.models.NewRecentMatches1.objects.values('id_match4').distinct()
                mat_id = tether.models.NewRecentMatches1.objects.filter(userprofile1__steam_id=sid).values_list(
                    'id_match4').distinct()

                print(mid)
                print(mat_id)

                a = mat_id
                mat_id = " ".join([x[0] for x in a])
                print(mat_id)

                match_ini = api.get_match_details(match_id=mat_id)
                wanted = set(match_ini) - {'game_mode_name', 'human_players', 'match_id', 'game_mode', 'duration',
                                           'lobby_type', 'lobby_name', 'engine', 'start_time', 'cluster'}
                common_gd = match_ini
                for unwanted_key in wanted:
                    del common_gd[unwanted_key]

                {'match_id': str(k) for k, v in common_gd.items()}
                cd = tether.models.CommonData(**common_gd)
                cd.save()
                print(common_gd)

            # get_common_d()

            def get_dota_d(self):

                mid = tether.models.NewRecentMatches1.objects.values('id_match4').distinct()
                mat_id = tether.models.NewRecentMatches1.objects.filter(userprofile1__steam_id=sid).values_list(
                    'id_match4').distinct()

                print(mid)
                print(mat_id)

                a = mat_id
                mat_id = " ".join([x[0] for x in a])
                print(mat_id)

                ini2 = api.get_match_details(
                    match_id=mat_id)  # tether.models.NewRecentMatches.objects.values('id_match0'))  # copying the match_ini dictionary does not work, for unknown reason.
                wanted2 = set(ini2) - {'match_id', 'leagueid', 'tower_status_radiant', 'first_blood_time',
                                       'positive_votes', 'radiant_win', 'tower_status_dire', 'dire_score',
                                       'pre_game_duration', 'flags', 'cluster_name', 'radiant_score',
                                       'barracks_status_radiant', 'match_seq_num', 'barracks_status_dire',
                                       'negative_votes'}
                dota2gd = ini2
                for unwanted_key in wanted2:
                    del dota2gd[unwanted_key]

                {'match_id': str(k) for k, v in dota2gd.items()}

                dotad = tether.models.DotaData(**dota2gd)
                dotad.save()

                print(dota2gd)
                # get_dota_d()

        # -----------------------------------------------------------------------------------------------

        r = PlayersAndData()
        r.get_profile_match_hist()
        r.get_match_players()
        r.get_all_data()
        r.get_common_d()
        r.get_dota_d()
    # ------------------------------------------------------------------------------------------------------------
    # datatable = tether.tables.PlayerData(tether.models.MatchData.objects.filter(id=120))
    datatable = tether.tables.PlayerData(
        tether.models.MatchData.objects.raw('''SELECT * from match_data WHERE id >= 333'''))
    playertable = tether.tables.PlayerTable(
        tether.models.MatchPlayers.objects.filter(newrecentmatches1__userprofile1__steam_id=sid), prefix='1-')
    table = tether.tables.MatchTable(tether.models.NewRecentMatches1.objects.filter(userprofile1__steam_id=sid),
                                     prefix='2-')
    RequestConfig(request).configure(table)
    RequestConfig(request).configure(playertable)
    # Manual / force id value
    # table = tether.tables.MatchTable(tether.models.NewRecentMatches1.objects.filter(id=1))
    # table = tether.tables.MatchTable(tether.models.NewRecentMatches1.objects.filter(players__newrecentmatches1__userprofile1__steam_id=101869174))

    # usr=request.user.id
    # {'playertable': playertable})
    if request.method == 'POST':
        view_wanted = request.POST.get('view_wanted')

        return render(request, 'tether/user_profile.html', {'table': table,
                                                            'playertable': playertable,
                                                            'playerdata': datatable})

    return render(request, 'tether/user_profile.html', {'table': table,
                                                        'playertable': playertable,
                                                        'playerdata': datatable})


def matchplayers(request):
    playertable = tether.tables.PlayerTable(
        tether.models.MatchPlayers.objects.filter(newrecentmatches1__userprofile1__steam_id=profile.sid), prefix='1-')
    RequestConfig(request).configure(playertable)

    if request.method == 'POST':
        view_wanted = request.POST.get('view_wanted')
        return render(request, {'playertable': playertable})

    return render(request, {playertable: playertable})

    # Updating Profiles
    # if request.method == 'POST':
    # user_form = UserForm(request.POST)
    # profile_form = UserProfileForm(request.POST)
    # if user_form.is_valid() and profile_form.is_valid():
    # initial_data = user_form.save()

    # Hashing the password
    # initial_data.set_password(initial_data.password)
    # initial_data.save()

    # Saving userprofile information
    # profile = profile_form.save(commit=False)
    # profile.user = user

    # profile.save()
    # messages.success(request, 'Your profile was successfully updated!')
    # return redirect('settings:profile')
    # else:
    # messages.error(request, 'Please correct the following error(s)')
    # else:
    # user_form = UserForm
    # profile_form = UserProfileForm
    # return render(request, 'tether/user_profile.html', {
    # 'user_form': user_form,
    # 'profile_form': profile_form
    # })


def intro(request):
    return render(request, "tether/intro.html")
