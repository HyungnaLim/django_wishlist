from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'),   # home page
    path('about', views.about, name='about'),
    path('visited', views.places_visited, name='places_visited')
]