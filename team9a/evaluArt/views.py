from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from evaluArt.forms import UserForm, UserProfileForm, ContactUsForm, ArtworkForm
from evaluArt.models import ContactUs, Comments, Rating, Category, Artwork, UserProfile
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


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
                return redirect(reverse('evaluArt:login'))
                
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
        f = ArtworkForm(request.POST, request.FILES)
        if f.is_valid():
            f.save()
            img_obj = f.instance
            messages.add_message(request, messages.INFO, 'Artwork Submitted.')
            return render(request, 'upload_artwork.html', {'form': f, 'img_obj': img_obj})
    else:
        f = ArtworkForm()
    return render(request, 'evaluArt/upload_artwork.html', {'form': f})

def artwork_list(request):
    artwork = Artwork.objects.all()
    return render(request, 'evaluArt/artwork_list.html', {'artwork': artwork})


@login_required
def my_account(request):

    context_dict = {}
    context_dict['user'] = request.user
    context_dict['profile'] = UserProfile.objects.filter(user = context_dict['user'])[0]
    context_dict['artwork'] = Artwork.objects.filter(user = context_dict['profile'])

    initial_data = {
        'picture': context_dict['profile'].picture,
        'experience': context_dict['profile'].experience,
        'description': context_dict['profile'].description
    }

    form = UserProfileForm(instance=context_dict['profile'])


# if the request is to POST a form
    if request.method == 'POST':
        update_form = UserProfileForm(request.POST, instance=context_dict['profile'])
        if update_form.is_valid:
            update_form.save()
            return redirect(reverse('evaluArt:my_account'))

# request doesnt post a form
    else:
        context_dict['update_details'] = form

    return render(request, 'evaluArt/my_account.html', context=context_dict)


