from tether.models import UserProfile, League
from django.contrib.auth.models import User
from django import forms


# The form for user profiles
class UserForm(forms.ModelForm):
    # Keeps the password hidden while typing
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


# Additional form for more attributes to user profile.
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('region',)


class LeagueForm(forms.ModelForm):
    league_name = forms.CharField(max_length=255, help_text="Enter the name of the League.")
    region = forms.CharField(max_length=255, help_text="Enter the region of the League.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = League
        fields = ('league_name', 'region', 'slug')
