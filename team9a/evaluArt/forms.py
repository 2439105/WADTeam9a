from django import forms
from django.contrib.auth.models import User
from evaluArt.models import UserProfile, ContactUs

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class ContactUs(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'