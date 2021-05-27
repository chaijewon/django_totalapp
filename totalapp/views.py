from django.shortcuts import render,redirect
from totalapp import models
# Create your views here.
def home(request):
    try:
         page=request.GET['page']
         curpage=int(page)
    except Exception as e:
          curpage=1
    movie_data=models.movie_list(curpage)
    md=[]
    for row in movie_data:
        data={"mno":row[0],"poster":row[1],"title":row[2]}
        md.append(data)

    block=5
    startPage=((curpage-1)//block*block)+1
    endPage=((curpage-1)//block*block)+block
    totalpage=models.movie_totalpage()
    totalpage=int(totalpage)
    if endPage>totalpage:
        endPage=totalpage

    print("startPage="+str(startPage))
    print("endPage="+str(endPage))

    return render(request,'total/home.html',{"curpage":curpage,"totalpage":totalpage,"startPage":startPage,"endPage":endPage,"md":md,"range":range(startPage,endPage+1)})
#mno,poster,title,regdate,genre,nation,grade,time,score,showuser,boxoffice,story,key
def movie_detail(request):
     mno=request.GET['mno']
     md=models.movie_detail(int(mno))
     print(md)
     movie_data={
         "mno":md[0],
         "poster":md[1],
         "title":md[2],
         "regdate":md[3],
         "genre":md[4],
         "nation":md[5],
         "grade":md[6],
         "time":md[7],
         "score":md[8],
         "showuser":md[9],
         "boxoffice":md[10],
         "story":md[11],
         "key":md[12]
     }
     return render(request,'total/movie_detail.html',movie_data)
#no,title,singer,album,poster,state,idcremen
def music(request):
    try:
          page=request.GET['page']
          curpage=int(page)
    except Exception as e:
           curpage=1
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
    # 페이지를 받는다 = 없는 경우에 except를 수행 => curpage=1
    try:
         page=request.GET['page']
         curpage=int(page)
    except Exception as e:
         curpage=1

    recipe_data=models.recipe(curpage)
    totalpage=models.recipe_totalpage()
    count=models.recipe_count()

    # 딕트 {키:값}
    rd=[]
    for row in recipe_data:
        data={"no":row[0],"title":row[2],"poster":row[1],"chef":row[3]}
        rd.append(data)

    block=10
    startPage=((curpage-1)//block*block)+1  # curpage=1~10  => 1,2,3,4,5,6,7,8,9,10   ( 1, 11 ,21...)
    endPage=((curpage-1)//block*block)+block # 10 20 30 .... => 23  21 22 23
    if endPage>totalpage :
        endPage=totalpage

       # 마지막은 제외   <=(X) <10
    # html => {% for i in range %} => range를 사용할 수 없다
    data={"count":count,"curpage":curpage,"totalpage":totalpage,"startPage":startPage,"endPage":endPage,"rd":rd,"range":range(startPage,endPage+1)}
    return render(request,'total/recipe.html',data)
#레시피 상세보기
# poster,chef,chef_poster,title,content,info1,info2,info3,foodmake,chef_info
def recipe_detail(request):
    no=request.GET['no']
    detail_data=models.recipe_detail(int(no))
    fm=detail_data[8].split('\n')
    for f in fm:
        print(f)
    dd={"poster":detail_data[0],"chef":detail_data[1],"chef_poster":detail_data[2],
          "title":detail_data[3],"content":detail_data[4],"info1":detail_data[5],
          "info2":detail_data[6],"info3":detail_data[7],
          "foodmake":fm,"chef_info":detail_data[9]}
    # {"dd":dd} => dd.poster
    return render(request,'total/recipe_detail.html',dd)

def chef(request):
    chef_name=request.GET['chef']
    try:
        page=request.GET['page']
        curpage=int(page)
    except Exception as e:
        curpage=1

    chef_recipe=models.chef_list(chef_name,curpage)
    totalpage=models.chef_totalpage(chef_name)
    count=models.chef_count(chef_name)
    rd = []
    for row in chef_recipe:
        data = {"no": row[0], "title": row[2], "poster": row[1], "chef": row[3]}
        rd.append(data)

    block = 10
    startPage = ((curpage - 1) // block * block) + 1  # curpage=1~10  => 1,2,3,4,5,6,7,8,9,10   ( 1, 11 ,21...)
    endPage = ((curpage - 1) // block * block) + block  # 10 20 30 .... => 23  21 22 23
    if endPage > totalpage:
        endPage = totalpage

    # 마지막은 제외   <=(X) <10
    # html => {% for i in range %} => range를 사용할 수 없다
    data = {"count": count, "curpage": curpage, "totalpage": totalpage, "startPage": startPage, "endPage": endPage,
              "rd": rd, "range": range(startPage, endPage + 1),"chef":chef_name}
    return render(request,'total/chef.html',data)














