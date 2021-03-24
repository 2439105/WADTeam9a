from django.urls import path
from evaluArt import views
from .views import PostListView, UserPostListView, PostDetailView

app_name = 'evaluArt'

urlpatterns = [
    path('', PostListView.as_view(), name='home'),  # url for post list.
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),  # url for specific user post.
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # url for post detail.
    
    path('register/', views.register, name='register'), # New mapping
    path('login/', views.user_login, name='login'),
    path('canvas/', views.canvas, name='canvas'),
    path('logout/', views.user_logout, name='logout'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('contact_us/evaluArt/', views.base, name='base'), #This redirects to the home page from the contact us page. I will fix this later.
]
