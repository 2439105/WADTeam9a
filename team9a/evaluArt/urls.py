from django.urls import path
from evaluArt import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'evaluArt'

urlpatterns = [
    path('', views.artwork_list, name='artwork_list'),  # url for post list.
    path('upload_artwork/', views.upload_artwork, name='upload_artwork'),

    # take in variable as pk for artwork
    path('artwork/<int:pk>/', views.show_artwork, name='show_artwork'),
    
    path('register/', views.register, name='register'), # New mapping
    path('login/', views.user_login, name='login'),
    path('canvas/', views.canvas, name='canvas'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.about, name='about'),
    path('my_account/', views.my_account, name='my_account'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('contact_us/evaluArt/', views.base, name='base'), #This redirects to the home page from the contact us page. I will fix this later.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)