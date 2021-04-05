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
        {"name": "Abstract"},
        {"name": "Animals"},
        {"name": "Anime Cartoons"},
        {"name": "Futuristic"},
        {"name": "Surrealism"},
        {"name": "Pixel Art"},
        {"name": "Nature"},
        {"name": "Human"}
    ]

    for c in cats:
        add_cat(c['name'])

    #Create users. Must be equal number of users and userprofiles
    
    users = [
        {"username":"pabloPicasso", "email":"picasso@gmail.com", "password":"oldguitarist1903"},
        {"username":"artStudent", "email":"artStudent@gmail.com", "password":"iloveart"},
        {"username":"professorMimi", "email":"MimiSmith@gmail.com", "password":"pastelqueen43"},
        {"username":"amateurArtist", "email":"amateur@gmail.com", "password":"justheretolearn"},
        ]
    userprofiles = [
        {"experience":"3", "picture":"populate_database/pablopicasso.jpeg", "description":"Skilled surrealist artist that specialises in painting, scuplting, and ceramics."},
        {"experience":"1", "picture":"populate_database/artStudent.jpeg", "description":"I love drawing and painting and would like to get more advice as I develop my skills in university."},
        {"experience":"2", "picture":"populate_database/professor.jpeg", "description":"I adore teaching and want to share my knowledge of art with those who want to improve their skills and understanding."},
        {"experience":"0", "picture":"populate_database/amateur.jpeg", "description":"In my free time, I like to draw. I want to be able to draw more diverse subjects accurately."},
        ]
    
    count = 0
    for user in users:
        created_user = User.objects.create_user(user.get("username"), user.get("email"), user.get("password"))
        userprofiles[count]["user"] = created_user
        count += 1
    
    for user in userprofiles:
        add_userprofile(user.get("user"),user.get("experience"),user.get("picture"),user.get("description"))

    artwork = [
        {"picture":"populate_database/face.jpeg", "description":"What do you think of the colors I used here? I like the concept but not sure if I pulled it off.", "user":"artStudent", "category":"Human"},
        {"picture":"populate_database/birds.jpeg", "description":"I'm not sure what to do for the background here. Any advice?", "user":"professorMimi", "category":"Nature"},
        {"picture":"populate_database/colors.jpeg", "description":"How did this one turn out?", "user":"artStudent", "category":"Surrealism"},
        {"picture":"populate_database/hill.jpeg", "description":"My newest nature drawing", "user":"professorMimi", "category":"Nature"},
        {"picture":"populate_database/landscape.jpeg", "description":"Can you give me some advice on layers/background?", "user":"amateurArtist", "category":"Nature"},
        {"picture":"populate_database/smallWaterfall.jpeg", "description":"What is the best way to draw flowing water?", "user":"amateurArtist", "category":"Nature"}
        ]
    for art in artwork:
        add_artwork(art.get("picture"), art.get("description"), art.get("user"), art.get("category"))
    
    comments = [
        {"user":"professorMimi", "artwork":"populate_database/smallWaterfall.jpeg","text":"Use small brush strokes and pay careful attention to the way water moves. Use many different colors to show depth."},
        {"user":"professorMimi", "artwork":"populate_database/landscape.jpeg","text":"Try to work with shadow and light to create a greater sense of depth."},
        {"user":"professorMimi", "artwork":"populate_database/colors.jpeg","text":"I love the colors! It looks very bright and happy."},
        {"user":"professorMimi", "artwork":"populate_database/face.jpeg","text":"Very accurate drawing of a face. Perfect capture of emotion."},
        {"user":"artStudent", "artwork":"populate_database/smallWaterfall.jpeg","text":"Try to use a variety of colors. I think the river banks are really cool though."},
        {"user":"artStudent", "artwork":"populate_database/birds.jpeg","text":"I love the detail! Maybe a background of tree branches or a bright blue sky would fit."},
        ]
    for comment in comments:
        add_comment(comment.get("user"), comment.get("artwork"), comment.get("text"))
        
    ratings = [
        {"user":"pabloPicasso", "artwork":"populate_database/smallWaterfall.jpeg", "number":2},
        {"user":"professorMimi", "artwork":"populate_database/smallWaterfall.jpeg", "number":2},
        {"user":"artStudent", "artwork":"populate_database/smallWaterfall.jpeg", "number":3},
        {"user":"pabloPicasso", "artwork":"populate_database/birds.jpeg", "number":3},
        {"user":"artStudent", "artwork":"populate_database/birds.jpeg", "number":4},  
        {"user":"pabloPicasso", "artwork":"populate_database/face.jpeg", "number":4},
        {"user":"professorMimi", "artwork":"populate_database/face.jpeg", "number":5},
        {"user":"amateurArtist", "artwork":"populate_database/face.jpeg", "number":5},
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
    
def add_artwork(art, description, username, category):
    cat = Category.objects.filter(name=category)[0]
    user = User.objects.filter(username=username)[0]
    userprofile = UserProfile.objects.filter(user = user)[0]
    a = Artwork.objects.get_or_create(picture=art, description = description, date_posted = timezone.now(), user = userprofile, category = cat)[0]
    a.save()
    print("Added a new artwork")
    
def add_comment(username, artwork, text):
    artwork = Artwork.objects.filter(picture = artwork)[0]
    user = User.objects.filter(username=username)[0]
    userprofile = UserProfile.objects.filter(user = user)[0]
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
    
    