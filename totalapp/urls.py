from django.urls import path
from totalapp import  views

urlpatterns=[
    path('',views.home),
    path('movie_detail/',views.movie_detail),
    path('music/',views.music),
    path('recipe/',views.recipe),
    path('chef/',views.chef),
    path('recipe_detail/',views.recipe_detail),
    path('food/',views.food),
    path('food_list/',views.food_list),
    path('food_detail/',views.food_detail)
]