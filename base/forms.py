from django import forms
from django.forms import ModelForm
from .models import Room,UserProfile
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']






class UserForm(ModelForm):
    class Meta:
        model = User   
        fields = ['username','email',]     


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile   
        fields = ['bio','avatar',]             