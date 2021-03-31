import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team9a.settings')

import django
django.setup()
from evaluArt.models import UserProfile, Category, Artwork, Comments, Rating



def populate():
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

    
def add_cat(name):
    c = Category.objects.get_or_create(name = name)[0]
    c.save()
    print("Added a new category - {}".format(name))


if __name__ == '__main__':
    print("Populating evaluArt with categories: ")
    populate()