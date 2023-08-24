from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User
from django import forms


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'password1', 'password2',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'avatar',)


class PasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ('password1', 'password2')
