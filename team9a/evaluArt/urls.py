from django.urls import path
from evaluArt import views

app_name = 'evaluArt'

urlpatterns = [
    path('', views.base, name='base'),
    path('register/', views.register, name='register'), # New mapping
    path('login/', views.user_login, name='login'),
    path('canvas/', views.canvas, name='canvas'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('contact_us/evaluArt/', views.base, name='base'), #This redirects to the home page from the contact us page. I will fix this later.
]
