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
    
class Post(models.Model):
    #artwork_id = models.IntegerField(primary_key=True)
    picture = models.ImageField()
    content = models.CharField(max_length = 800)
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + self.picture

    def get_absolute_url(self):
        """
            Creates the absolute url for a particular post.
        """
        return reverse('blog:post-detail', kwargs={'pk': self.pk})
    '''
class Artwork(models.Model):
    artwork_id = models.IntegerField(primary_key=True)
    picture = models.ImageField()
    description = models.CharField(max_length = 800)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + self.picture
'''
class comments(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ': ' +   self.text
    
class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Post, on_delete=models.CASCADE)
    number = models.IntegerField()
    def __str__(self):
        return self.user.username + self.number
   
#implement categories in other models later
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    

    