from tether.models import UserProfile1, League
from django.contrib.auth.models import User
from django import forms


# The form for user profiles
class UserForm(forms.ModelForm):
    # Keeps the password hidden while typing
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control input-md'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-md'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-md'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email']


# Additional form for more attributes to user profile.
class UserProfileForm(forms.ModelForm):
    region = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-md'}))

    class Meta:
        model = UserProfile1
        fields = ('region',)


class LeagueForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = League
        fields = ('league_name', 'region', 'skill_level', 'password', 'slug')
