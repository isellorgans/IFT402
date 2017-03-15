from tether.forms import UserForm, UserProfileForm, LeagueForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user
from tether.models import League, UserProfile1
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from django_tables2 import RequestConfig
from tether.tables import LeagueTable
from django.views.generic.edit import CreateView


def index(request):
    context = dict()

    try:
        l = League.objects.annotate(user_count=Count('userprofile')).order_by('-user_count')[:5]

        context['leaguename0'] = l[0].league_name
        context['leagueregion0'] = l[0].region
        context['leagueplayers0'] = l[0].userprofile_set.count() + 1

        context['leaguename1'] = l[1].league_name
        context['leagueregion1'] = l[1].region
        context['leagueplayers1'] = l[1].userprofile_set.count() + 1

        context['leaguename2'] = l[2].league_name
        context['leagueregion2'] = l[2].region
        context['leagueplayers2'] = l[2].userprofile_set.count() + 1

        context['leaguename3'] = l[3].league_name
        context['leagueregion3'] = l[3].region
        context['leagueplayers3'] = l[3].userprofile_set.count() + 1

        context['leaguename4'] = l[4].league_name
        context['leagueregion4'] = l[4].region
        context['leagueplayers4'] = l[4].userprofile_set.count() + 1

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
                return HttpResponseRedirect('/tether/')
            else:
                return HttpResponse("Your account is currently disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Your username or password was incorrect.")

    else:
        return render(request, "tether/login.html")


def public_leagues(request, league_name_slug):
    context_dict = {}

    # try:
    league = League.objects.get(slug=league_name_slug)
    context_dict['league'] = league

    # admin = League.objects.get(league.name).values()
    # context_dict['admin'] = admin

    # except League.DoesNotExist:
    # context_dict['league'] = None

    return render(request, 'tether/public_leagues.html', context_dict)


def join_public(request):
    table = LeagueTable(League.objects.all())
    RequestConfig(request, paginate={'per_page': 20}).configure(table)

    return render(request, "tether/join_public.html", {'table': table})


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


    #Updating Profiles
    #if request.method == 'POST':
        #user_form = UserForm(request.POST)
        #profile_form = UserProfileForm(request.POST)
        #if user_form.is_valid() and profile_form.is_valid():
            #initial_data = user_form.save()

            #Hashing the password
            #initial_data.set_password(initial_data.password)
            #initial_data.save()

            #Saving userprofile information
            #profile = profile_form.save(commit=False)
            #profile.user = user

            #profile.save()
            #messages.success(request, 'Your profile was successfully updated!')
            #return redirect('settings:profile')
        #else:
            #messages.error(request, 'Please correct the following error(s)')
    #else:
        #user_form = UserForm
        #profile_form = UserProfileForm
    #return render(request, 'tether/user_profile.html', {
        #'user_form': user_form,
        #'profile_form': profile_form
    #})


def intro(request):
    return render(request, "tether/intro.html")
