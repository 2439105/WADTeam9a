import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team9a.settings')

import django
django.setup()
from evaluArt.models import UserProfile, Category, Artwork, Comments, Rating
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File
#python manage.py help flush

def populate():
    #Populate the categories
    cats = [
        {"name": "abstract"},
        {"name": "animals"},
        {"name": "anime_cartoons"},
        {"name": "futuristic"},
        {"name": "surrealism"},
        {"name": "pixel art"},
        {"name": "nature"}
    ]

    for c in cats:
        add_cat(c['name'])

    #Create users. Must be equal number of users and userprofiles
    
    users = [
        {"username":"pabloPicasso", "email":"picasso@gmail.com", "password":"oldguitarist1903"}
        ]
    userprofiles = [
        {"experience":"3", "picture":"populateImg/pablopicasso.jpeg", "description":"Skilled surrealist artist that specialises in painting, scuplting, and ceramics."}
        ]
    
    count = 0
    for user in users:
        created_user = User.objects.create_user(user.get("username"), user.get("email"), user.get("password"))
        userprofiles[count]["user"] = created_user
        count += 1
    
    for user in userprofiles:
        add_userprofile(user.get("user"),user.get("experience"),user.get("picture"),user.get("description"))

    artwork = [
        {"picture":"populateImg/leReve.jpeg", "description":"sleeping woman", "user":"pabloPicasso", "category":"surrealism"}
        ]
    for art in artwork:
        '''
        file = open(art.get("picture"), 'w')
        artwork = File(file)
        '''
        add_artwork(art.get("picture"), art.get("description"), art.get("user"), art.get("category"))
    
    
    comments = [
        {"user":"pabloPicasso", "artwork":"populateImg/leReve.jpeg","text":"Beautiful painting, with very unique style."}
        ]
    for comment in comments:
        add_comment(comment.get("user"), comment.get("artwork"), comment.get("text"))
        
    ratings = [
        {"user":"pabloPicasso", "artwork":"populateImg/leReve.jpeg", "number":4}
        ]
    for rating in ratings:
        add_rating(rating.get("user"), rating.get("artwork"), rating.get("number"))


def add_cat(name):
    c = Category.objects.get_or_create(name = name)[0]
    c.save()
    print("Added a new category - {}".format(name))
    
def add_userprofile(user, experience, picture, description):
    p = UserProfile.objects.get_or_create(user = user, experience = experience, picture=picture, description=description)[0]
    p.save()
    print("Added a new user profile - {}".format(user.username))
    
def add_artwork(picture, description, username, category):
    cat = Category.objects.filter(name=category)[0]
    user = User.objects.filter(username=username)[0]
    userprofile = UserProfile.objects.filter(user = user)[0]
    a = Artwork.objects.get_or_create(picture = picture, description = description, date_posted = timezone.now(), user = userprofile, category = cat)[0]
    a.save()
    print("Added a new artwork")
    
def add_comment(username, artwork, text):
    user = User.objects.filter(username=username)[0]
    userprofile = UserProfile.objects.filter(user = user)[0]
    artwork = Artwork.objects.filter(picture = "populateImg/leReve.jpeg")[0]
    c = Comments.objects.get_or_create(user = userprofile, artwork = artwork, text = text, date = timezone.now())[0]
    c.save()
    print("Added a new comment - {}".format(text))

def add_rating(username, artwork, number):
    user = User.objects.filter(username=username)[0]
    userprofile = UserProfile.objects.filter(user = user)[0]
    artwork = Artwork.objects.filter(picture = artwork)[0]
    r = Rating.objects.get_or_create(user = userprofile, artwork=artwork, number = number)[0]
    r.save()
    print("Added a new rating - {}".format(number))


if __name__ == '__main__':
    print("Populating evaluArt with categories: ")
    populate()