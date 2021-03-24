from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from evaluArt.forms import UserForm, UserProfileForm
from evaluArt.models import ContactUs, comments, Rating, Category, Post
from django.shortcuts import redirect
from django.contrib import messages

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json

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

def canvas(request):
    return render(request, 'evaluArt/canvas.html')


def contact_us(request):
    if request.method == 'POST':
        f = ContactUs(request.POST)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'Feedback Submitted.')
            #REDIRECT TO HOME PAGE LATER
            return redirect('evaluArt/')
    else:
        f = ContactUs()    
    return render(request, 'evaluArt/contact_us.html', {'form': f })

class PostListView(ListView):
    model = Post
    template_name = 'evaluArt/artwork.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'evaluArt/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(UserProfile, user=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

'''
#This shows all posts in order of newest first. Each page displays 15 posts and we move to the next apge to view more
class PostListView(ListView):
	model = Artwork
	template_name = 'evaluArt/artwork.html'
	context_object_name = 'artwork'
	ordering = ['-date_posted']
	paginate_by = 15
	def get_context_data(self, **kwargs):
		context = super(PostListView, self).get_context_data(**kwargs)
        #if user is signed in this shows if they have rated the post
		if self.request.user.is_authenticated:
			rated = [i for i in Artwork.objects.all() if Rating.objects.filter(user = self.request.user, post=i)]
			context['rated_post'] = rated
		return context
    
#Shows all posts by specific user
class UserPostListView(LoginRequiredMixin, ListView):
	model = Artwork
	template_name = 'evaluArt/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 15

	def get_context_data(self, **kwargs):
		context = super(UserPostListView, self).get_context_data(**kwargs)
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		rated = [i for i in Artwork.objects.filter(user_name=user) if Rating.objects.filter(user = self.request.user, post=i)]
		context['liked_post'] = rated
		return context

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Artwork.objects.filter(user_name=user).order_by('-date_posted')
#shows a single post and allows a user to comment
@login_required
def post_detail(request, pk):
	artwork = get_object_or_404(Artwork, pk=pk)
	user = request.user
	is_rated =  Rating.objects.filter(user=user, artwork=Artwork)
	if request.method == 'POST':
		form = NewCommentForm(request.POST)
		if form.is_valid():
			data = form.save(commit=False)
			data.artwork = artwork
			data.username = user
			data.save()
			return redirect('post-detail', pk=pk)
	else:
		form = NewCommentForm()
	return render(request, 'evaluArt/post_detail.html', {'artwork':artwork, 'is_rated':is_rated, 'form':form})

#rating system change with comments

@login_required
def like(request):
	artwork_id = request.GET.get("likeId", "")
	user = request.user
	post = Artwork.objects.get(pk=artwork_id)
	rated= False
	rated = Rating.objects.filter(user=user, artwork=Artwork)
	if rated:
		rated.delete()
	else:
		liked = True
		Like.objects.create(user=user, post=post)
	resp = {
        'liked':liked
    }
	response = json.dumps(resp)
	return HttpResponse(response, content_type = "application/json")
'''