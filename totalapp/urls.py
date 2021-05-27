from django.urls import path
from totalapp import  views

urlpatterns=[
    path('',views.home),
    path('movie_detail/',views.movie_detail),
    path('music/',views.music),
    path('food/',views.food),
    path('recipe/',views.recipe),
    path('chef/',views.chef),
    path('recipe_detail/',views.recipe_detail)
]