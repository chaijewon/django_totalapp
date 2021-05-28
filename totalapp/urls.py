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
    path('food_detail/',views.food_detail),
    path('news/',views.newsData),
    path('board/list/',views.board_list),
    path('board/insert/',views.board_insert),
    path('board/insert_ok/',views.board_insert_ok),
    path('board/detail/',views.board_detail),
    path('board/update/',views.board_update_data),
    path('board/update_ok/',views.board_update_ok),
    path('board/reply/',views.board_reply),
    path('board/reply_ok/',views.board_reply_ok),
    path('board/delete/',views.board_delete),
    path('board/delete_ok/',views.board_delete_ok)
]