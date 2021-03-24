from django import forms
from django.contrib.auth.models import User
from evaluArt.models import UserProfile, ContactUs, comments, Post

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
  
#maybe delete these
'''
class NewArtworkForm(forms.ModelForm):
	class Meta:
		model = Artwork
		fields = ['picture', 'description']

class NewCommentForm(forms.ModelForm):
	class Meta:
		model = comments
		fields = ['text']
        '''