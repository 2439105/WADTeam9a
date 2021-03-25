from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # The additional attributes we wish to include.
    #website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    
    def __str__(self):
        return self.user.username
    
class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Feedback"

    def __str__(self):
        return self.name + "-" +  self.email
    
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Artwork(models.Model):
    #artwork_id = models.IntegerField(primary_key=True)
    picture = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)
    content = models.CharField(max_length = 800)
    date_posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.user + self.picture

    def get_absolute_url(self):
        return reverse('evaluArt:artwork-detail', kwargs={'pk': self.pk})

class comments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' +   self.text
    
class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    number = models.IntegerField()
    def __str__(self):
        return self.user.username + self.number
       