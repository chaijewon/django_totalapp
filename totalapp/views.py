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

#맛집
def food(request):
    #no,title,subject,poster
    fd1=models.food_category(1,12)
    #믿고 보는 맛집 리스트
    f1=[]
    for ff in fd1:
        fd_data1={"no":ff[0],"title":ff[1],"subject":ff[2],"poster":ff[3]}
        f1.append(fd_data1)

    #지역별 인기 맛집
    f2=[]
    fd2=models.food_category(13,18)
    for ff in fd2:
         fd_data2 = {"no": ff[0], "title": ff[1], "subject": ff[2], "poster": ff[3]}
         f2.append(fd_data2)

    #메뉴별 인기 맛집
    f3=[]
    fd3=models.food_category(19,30)
    for ff in fd3:
         fd_data3 = {"no": ff[0], "title": ff[1], "subject": ff[2], "poster": ff[3]}
         f3.append(fd_data3)

    return render(request,'total/food.html',{"fd1":f1,"fd2":f2,"fd3":f3})

def food_list(request):
      cno=request.GET['cno']
      #데이터베이스 연동  no,poster,title,address,tel
      food_data=models.food_list(int(cno))
      fd=[]
      for ff in food_data:
          ss=ff[1].split("^")
          data={"no":ff[0],"title":ff[2],"address":ff[3],"tel":ff[4],"poster":ss[0]}
          fd.append(data)
      return render(request,'total/food_list.html',{"fd":fd})
'''
  1. RequestMapping(GetMapping,PostMapping) => urls.py  (URI,호출할 함수 지정)
  2. views.py => 함수제작 (요청값을 받아서 데이터베이스 연동후에 결과값을 html로 전송)
  3. models.py => DAO
  4. Templates : HTML,JSP  => {{값}} => {{}}:Vue.js == {{}}:AngularJS == {}:React.JS
     IT 
     = 퍼블리셔  : HTML,CSS (화면 디자인)
     =================================================
     = Front 개발자 : JavaScript (NodeJS,VueJS,ReactJS,AngularJS....) TypeScript
     = Back 개발자 : Spring , MyBtais , Java , 파이썬 ... (AI) 
     =================================================(+) Full Stack
     = DataBase 개발자 : 요구사항 분석, 설계 , 테이블 제작 ....
'''
def food_detail(request):
      no=request.GET['no']
      #db연동
      detail_data=models.food_detail(int(no))
      # poster,title,score,address,tel,type,price,parking,time,menu,good,soso,bad
      posters=detail_data[0].split("^")
      print(posters)
      menu=detail_data[9].split("원")
      address=detail_data[3].split("지")
      dd={
               "poster":posters,
               "title":detail_data[1],
               "score":detail_data[2],
               "address":address[0],
               "tel":detail_data[4],
               "type":detail_data[5],
               "price":detail_data[6],
               "parking":detail_data[7],
               "time":detail_data[8],
               "menu":menu,
               "good":detail_data[10],
               "soso":detail_data[11],
               "bad":detail_data[12]
           }
      return render(request,'total/food_detail.html',dd)














