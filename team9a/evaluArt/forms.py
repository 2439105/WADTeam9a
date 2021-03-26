from django import forms
from django.contrib.auth.models import User
from evaluArt.models import UserProfile, ContactUs, comments, Artwork

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture','experience',)

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
  
class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = '__all__'