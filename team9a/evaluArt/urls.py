from django.urls import path
from evaluArt import views

app_name = 'evaluArt'

urlpatterns = [
    path('', views.base, name='base'),
]