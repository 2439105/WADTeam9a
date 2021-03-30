from django.urls import path
from evaluArt import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'evaluArt'

urlpatterns = [
    path('', views.base, name='home'),  # url for post list.
    
    path('upload_artwork/', views.upload_artwork, name='artwork_create'),
    path('artwork/', views.artwork_list, name='artwork_list'),
    
    path('register/', views.register, name='register'), # New mapping
    path('login/', views.user_login, name='login'),
    path('canvas/', views.canvas, name='canvas'),
    path('logout/', views.user_logout, name='logout'),
    path('my_account/', views.my_account, name='my_account'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('contact_us/evaluArt/', views.base, name='base'), #This redirects to the home page from the contact us page. I will fix this later.
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)