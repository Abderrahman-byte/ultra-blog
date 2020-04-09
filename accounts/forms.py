from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Profil

class CreateUserForm(UserCreationForm) :
    class Meta :
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UpdateProfilForm(forms.ModelForm) :
    class Meta :
        model = Profil
        fields = '__all__'
        exclude = ['user', 'fav_tags']

class UpdateFavtagsForm(forms.ModelForm) :
    class Meta :
        model = Profil
        fields = ['fav_tags']