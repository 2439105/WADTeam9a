from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from evaluArt.forms import UserForm, UserProfileForm, ContactUsForm, ArtworkForm, CommentForm, SelectCategoryForm, RatingForm
from evaluArt.models import Comments, Rating, Category, Artwork, UserProfile
from django.contrib import messages

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


# Create your views here.
def base(request):
    return render(request, 'evaluArt/base.html')
    
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            profile = profile_form.save(commit=False)
            profile.user = user
            
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            registered = True
            
            return redirect(reverse('evaluArt:artwork_list'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                    'evaluArt/register.html',
                    context = {'user_form': user_form,
                                'profile_form': profile_form,
                                'registered': registered})
                                
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('evaluArt:artwork_list'))
                
            else:
                return HttpResponse("Your EvaluArt account is disabled.")
                
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    else:
        return render(request, 'evaluArt/login.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    return redirect(reverse('evaluArt:login'))
    
def about(request):
    return render(request, 'evaluArt/about.html')

def canvas(request):
    return render(request, 'evaluArt/canvas.html')

def contact_us(request):
    if request.method == 'POST':
        f = ContactUsForm(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            return redirect('/evaluArt')
    else:
        f = ContactUsForm()
    return render(request, 'evaluArt/contact_us.html', {'form': f})


@login_required
def upload_artwork(request):
    if request.method == 'POST':
        artwork_form = ArtworkForm(request.POST)
        if request.user.is_authenticated and artwork_form.is_valid():
            artwork = artwork_form.save(commit=False)
            if 'picture' in request.FILES:
                artwork.picture = request.FILES['picture']
            else:
                print('Requested picture is not in files.')
                print(artwork_form.errors)
            artwork.user = UserProfile.objects.filter(user=request.user)[0]
            selected_category = get_object_or_404(Category, pk=request.POST.get('category'))
            artwork.category = selected_category 
            artwork.save()
            return redirect(reverse('evaluArt:my_account'))
        else:
            print(artwork_form.errors)
    else:
        artwork_form = ArtworkForm()
    return render(request,  'evaluArt/upload_artwork.html', {'form': artwork_form})


def artwork_list(request):
    artwork = Artwork.objects.all()
    if request.method == 'POST':
        category_form = SelectCategoryForm(request.POST)
        if category_form.is_valid():
            selected_category = get_object_or_404(Category, pk=request.POST.get('category'))
            artwork = Artwork.objects.filter(category = selected_category)
    else:
        category_form = SelectCategoryForm()
    return render(request, 'evaluArt/artwork_list.html', {'form' : category_form, 'artwork': artwork})

def show_artwork(request, pk):

    # instances to pass into the html file
    artwork = Artwork.objects.filter(pk = pk)[0]
    profile = artwork.user
    comments = Comments.objects.filter(artwork=artwork)
    ratings = Rating.objects.filter(artwork=artwork)

    # find the average rating for a specific artwork
    total = 0
    count = 0
    average = 0
    # iterate through all ratings and sum them togeher then divide it by the number of ratings
    if ratings:
        for item in ratings:
            number = item.number
            total += number
            count += 1
        average = round(total/count, 2)

    context_dict={}
    context_dict['artwork'] = artwork
    context_dict['profile'] = profile
    context_dict['comments'] = comments
    context_dict['ratings'] = ratings
    context_dict['rating_num'] = count

    # if user is logged in, pass in the rating that the user previously voted
    if request.user.is_authenticated:
        try:
            loggedin = UserProfile.objects.filter(user=request.user)[0]
            prev = Rating.objects.filter(
                user=loggedin, 
                artwork = artwork)[0]
            context_dict['previous_rating'] = prev.number
        # catch index error as it means that the logged in user didnt rate the artwork before
        except IndexError:
            context_dict['previous_rating'] = "You haven't rate this artwork yet"


    
    context_dict['comment_form'] = CommentForm()
    context_dict['rating_form'] = RatingForm()
    context_dict['average_rating'] = average


    # check if post if from a comment form 
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'Comment' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.user = UserProfile.objects.filter(user = request.user)[0]
                    comment.artwork = context_dict['artwork']
                    comment.save()
                rating_form = RatingForm()
                return redirect(reverse('evaluArt:show_artwork', kwargs={'pk':pk}))


            elif 'Rate' in request.POST:
                rating_form = RatingForm(request.POST)
                if rating_form.is_valid():
                    rating_user = UserProfile.objects.filter(user=request.user)[0]
                    rating_artwork = context_dict['artwork']

                    try:
                        previous_rating = Rating.objects.filter(
                            user=rating_user, 
                            artwork = rating_artwork)[0]
                        previous_rating.number = rating_form.cleaned_data.get("number")
                        previous_rating.save()
                    except IndexError:
                        rating = rating_form.save(commit=False)
                        rating.user = rating_user
                        rating.artwork = rating_artwork
                        rating.save()

                comment_form = CommentForm()
                return redirect(reverse('evaluArt:show_artwork', kwargs={'pk':pk}))


    return render(request, 'evaluArt/show_artwork.html', context=context_dict)




@login_required
def my_account(request):
    # get all the fields for a profile, and all the artwork
    context_dict = {}
    context_dict['user'] = request.user
    context_dict['profile'] = UserProfile.objects.filter(user = context_dict['user'])[0]
    context_dict['artwork'] = Artwork.objects.filter(user = context_dict['profile'])
    context_dict['comments'] = Comments.objects.filter(artwork = context_dict['artwork'])

# initital data for the forms to change the user's profile details
    initial_data = {
        'picture': context_dict['profile'].picture,
        'experience': context_dict['profile'].experience,
        'description': context_dict['profile'].description
    }

# form to change profile details
# only to change profile picture, experience and description
    form = UserProfileForm(instance=context_dict['profile'])


# if the request is to POST a form
    if request.method == 'POST':
        update_form = UserProfileForm(request.POST, instance=context_dict['profile'])
        if update_form.is_valid:
            profile = update_form.save()

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
        
            return redirect(reverse('evaluArt:my_account'))

# request doesnt post a form
    else:
        context_dict['update_details'] = form

    return render(request, 'evaluArt/my_account.html', context=context_dict)


# view to show another user's account
def show_account(request, username):

    context_dict = {}
    context_dict['show_user'] = User.objects.get(username = username)
    context_dict['profile'] = UserProfile.objects.filter(user = context_dict['show_user'])[0]
    context_dict['artwork'] = Artwork.objects.filter(user = context_dict['profile'])
    context_dict['comments'] = Comments.objects.filter(artwork = context_dict['artwork'])
    return render(request, 'evaluArt/show_account.html', context=context_dict)


# view to query the database
def search(request):

    context_dict = {}

# get the word from the search form
    if request.method == 'POST':
        query = request.POST.get('query', None)
        if query!="":
            context_dict['query'] = query

# uses try-catch because there might not be a user whos username contains the query
            try:
                user_query = User.objects.filter(username__contains = query)[0]
                profile_query = UserProfile.objects.filter(user=user_query)
            except IndexError:
                profile_query = None
            finally:
                # this portion will always run
                # checks description of artwork, name of category, text of comments if it contains the query
                artwork_query = Artwork.objects.filter(description__contains = query)
                category_query = Category.objects.filter(name__contains = query)
                comments_query = Comments.objects.filter(text__contains = query)
            
            context_dict['profile_query'] = profile_query
            context_dict['artwork_query'] = artwork_query
            context_dict['category_query'] = category_query
            context_dict['comments_query'] = comments_query
            
    return render(request, 'evaluArt/search.html', context=context_dict)