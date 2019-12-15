from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password',
            'about',
            'why',
            'avatar',
            'position',
            'hd_status',
            'user_twitter',
            'date_joined',
            )
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'password',
            'about',
            'why',
            'avatar',
            'position',
            'hd_status',
            'user_twitter',
            'user_permissions',
            'date_joined'
            )
