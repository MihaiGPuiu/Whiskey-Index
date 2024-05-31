from django.urls import path 
from . import views
from .views import whiskey_list 
from .views import whiskey_of_the_day
from .views import irish 
from .views import japanese
from .views import bourbon
from .views import random_whiskey_search


urlpatterns = [
    path("", views.whiskey_list, name="home"),
    path('home/', whiskey_list, name='whiskey_list'),
    path('whiskey-of-the-day/', whiskey_of_the_day, name='whiskey_of_the_day'),
    path('irish/', irish, name='irish'),
    path('japanese/', japanese, name='japanese'),
    path('bourbon/', bourbon, name='bourbon'),
    path('random_whiskey_search/', views.random_whiskey_search, name='random_whiskey_search'),

] 
