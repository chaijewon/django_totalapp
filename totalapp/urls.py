from django.urls import path
from totalapp import  views

urlpatterns=[
    path('',views.home),
    path('music/',views.music),
    path('food/',views.food),
    path('recipe/',views.recipe)
]