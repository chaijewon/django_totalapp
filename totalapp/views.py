from django.shortcuts import render,redirect
from totalapp import models
# Create your views here.
def home(request):
    page=request.GET['page']
    curpage=int(page)
    movie_data=models.movie_list(curpage)
    md=[]
    for row in movie_data:
        data={"mno":row[0],"poster":row[1],"title":row[2]}
        md.append(data)
    return render(request,'total/home.html',{"md":md})
#no,title,singer,album,poster,state,idcremen
def music(request):
    page=request.GET['page']
    curpage=int(page)
    music_data=models.music_list(curpage) # 튜플
    md=[]
    for row in music_data:
        data={"no":row[0],"title":row[1],"singer":row[2],"album":row[3],"poster":row[4]}
        md.append(data)
    print(md)
    return render(request,'total/music.html',{"curpage":curpage,"totalpage":4,"md":md})

def food(request):
    return render(request,'total/food.html')

def recipe(request):
    return render(request,'total/recipe.html')
