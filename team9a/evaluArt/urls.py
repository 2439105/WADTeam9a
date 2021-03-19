from django.urls import path
from evaluArt import views

app_name = 'evaluArt'

urlpatterns = [
    path('', views.base, name='base'),
    path('register/', views.register, name='register'), # New mapping
    path('login/', views.user_login, name='login'),
    path('contact_us/', views.contact_us, name='contact_us'),
]