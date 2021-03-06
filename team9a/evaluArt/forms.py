from django import forms
from django.contrib.auth.models import User
from evaluArt.models import UserProfile, ContactUs, Comments, Artwork, Category, Rating

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture','experience','description')

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'
        
    def clean_user(self):
        if not self.cleaned_data['user']:
            return User()
        return self.cleaned_data['user']

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ('picture', 'description','category')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)

        widgets = {
            'text': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Post a comment...'}),
        }
        
class SelectCategoryForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('number', )
        