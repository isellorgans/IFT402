from tether.forms import UserForm, UserProfileForm, LeagueForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user, logout
from tether.models import League, UserProfile1, Matches
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django_tables2 import RequestConfig
from tether.tables import LeagueTable, ResultsTable
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.urls import NoReverseMatch


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
    context_dict = {}
    context_dict['matchbool'] = False

    league = League.objects.get(slug=league_name_slug)
    context_dict['league'] = league

    users = league.userprofile1_set.all()
    context_dict['users'] = users

    matches = league.matches_set.all()
    context_dict['matches'] = matches
    if context_dict['matches'] is not None:
        context_dict['matchbool'] = True
    #context_dict['matchurl'] = matches.id

    user = User.objects.get(pk=request.user.id)

    if league.password_status == 'Yes':
        context_dict['password'] = True

    if league.owner == user:
        context_dict['owner'] = True

    if request.method == 'POST':
        if 'join' in request.POST:
            if league.password_status == "Yes":
                if request.POST.get('password') == league.password:
                    user.userprofile1.leagues.add(league)
                    user.userprofile1.save()
                    league.save()
                else:
                    print("The password was incorrect.")
            else:
                user.userprofile1.leagues.add(league)
                user.userprofile1.save()
                league.save()
        elif 'make' in request.POST:
            m = request.POST.get('makefield')
            Matches.objects.create(lobby=league, name=m)

    return render(request, 'tether/public_leagues.html', context_dict)


@login_required()
def matches(request, match_id):
    context_dict = {}

    match = Matches.objects.get(id=match_id)
    context_dict['match'] = match
    p1 = None
    if request.method == 'GET':
        player1 = request.GET.get('player1_id')
        if player1:
            p1 = request.user
            match.player1 = p1
            match.save()

    return render(request, 'tether/matches.html', context_dict)


def join_public(request):
    results = None
    if request.method == 'GET':
        search_query = request.GET.get('search_box', None)
        if search_query is not None:
            results = ResultsTable(League.objects.filter(
                Q(league_name__icontains=search_query) |
                Q(region__icontains=search_query) |
                Q(skill_level__icontains=search_query) |
                Q(password_status__icontains=search_query) |
                Q(players__icontains=search_query)
            ))

    table = LeagueTable(League.objects.all())
    RequestConfig(request, paginate={'per_page': 20}).configure(table)

    return render(request, "tether/join_public.html", {'table': table, 'results': results})


@login_required(login_url='/tether/login/')
def add_league(request):
    if request.method == 'POST':
        form = LeagueForm(request.POST)
        user = User.objects.get(pk=request.user.id)

        if form.is_valid():
            forminstance = form.save(commit=False)
            forminstance.owner = user
            forminstance.save()
            return index(request)
        else:
            print(form.errors)
    else:
        form = LeagueForm()

    return render(request, 'tether/create.html', {'form': form})


@login_required(login_url='/tether/login/')
def profile(request):
    return render(request, 'tether/user_profile.html')


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
