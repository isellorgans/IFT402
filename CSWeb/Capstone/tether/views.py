from tether.forms import UserForm, UserProfileForm, LeagueForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user
from tether.models import League
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):
    return render(request, "tether/index.html", )


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

            # Hashing the password
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
    return render(request, "tether/join_public.html", )


@login_required(login_url='/tether/login/')
def add_league(request):
    form = LeagueForm()

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
    return render(request, 'tether/add_league.html', {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings:profile')
        else:
            messages.error(request, 'Please correct the following error(s)')
    else:
        user_form = UserForm
        profile_form = UserProfileForm
    return render(request, 'tether/user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



