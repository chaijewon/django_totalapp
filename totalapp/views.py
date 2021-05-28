from django.shortcuts import render,redirect
from totalapp import models
from urllib import parse
# 인코딩
import urllib.request as req
from bs4 import BeautifulSoup
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
      menu=''
      if detail_data[9]:
        menu=detail_data[9].split("원")
      else :
        menu='none'
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
'''
<title>하정우부터 황정민까지…넷플릭스 新시리즈 '수리남', 라인업 공개 [공식]</title>
<link>http://www.mydaily.co.kr/new_yk/html/read.php?newsid=202105280902799097&ext=na&utm_campaign=naver_news&utm_source=naver&utm_medium=related_news</link>
<description>
<![CDATA[ 드라마 '슬기로운 감빵생활', 영화 '양자물리학', 넷플릭스 '사냥의 시간', 하반기 공개 예정인 '오징어 게임'과... 개봉 예정인 영화 '발신제한'을 비롯해 영화 '봉오동 전투', '돈', '국가부도의 날', 드라마 '미스터 션샤인', '도깨비... ]]>
</description>
<pubDate>Fri, 28 May 2021 09:12:00 +0900</pubDate>
<author>마이데일리</author>
<category>연예</category>
<media:thumbnail url="https://imgnews.pstatic.net/image/thumb140/117/2021/05/28/3500662.jpg"/>
'''
def newsData(request):
    try:
         fd=request.POST['fd']
    except Exception as e:
         fd="영화"
    #인코딩
    fd=parse.quote(fd)
    url=f"http://newssearch.naver.com/search.naver?where=rss&query={fd}"
    result=req.urlopen(url)
    soup=BeautifulSoup(result,'html.parser')
    news_data=[]
    for item in soup.find_all("item"):
      pos=''
      try:
            title=item.find('title').string
            desc=item.find('description').string
            author=item.find('author').string
            category=item.find('category').string
            pos=item.find('media:thumbnail')
            poster=pos.get('url')
            print(title)
            print(desc)
            print(author)
            print(category)
            print(pos.get('url'))
            print('=================================================')
            data={"title":title,"desc":desc,"author":author,"category":category,"poster":poster}
            news_data.append(data)
      except Exception as e:
            pos='none'

    return render(request,'total/news.html',{"nd":news_data})

#답변형 게시판 관련
def board_list(request):
    try:
          page=request.GET['page']
          curpage=int(page)
    except Exception as e:
          curpage=1
    board_all_data=models.board_list(curpage)
    totalpage=models.board_totalpage()
    bd=[]
    for row in board_all_data:
        r=range(1,row[5]+1)
        print(r,row[5])
        data={"no":row[0],"subject":row[1],"name":row[2],"regdate":row[3],"hit":row[4],"range":r,"group_tab":row[5]}
        bd.append(data)
    return render(request,'total/board/list.html',{"curpage":curpage,"totalpage":totalpage,"list":bd})

def board_insert(request):
    return render(request,'total/board/insert.html')
def board_insert_ok(request):
    name=request.POST['name']
    subject=request.POST['subject']
    content=request.POST['content']
    pwd=request.POST['pwd']
    data=(name,subject,content,pwd)
    #DB연동
    models.board_insert(data)
    return redirect('/total/board/list/') #sendRedirect

# 배열 []=list => 이름부여  Object {}=dict (Map) 그냥
def board_detail(request):
    #no,name,subject,content,TO_CHAR(regdate,'YYYY-MM-DD'),hit
    no=request.GET['no'] #request.getParameter("no")
    detail_data=models.board_detail(int(no))
    dd={"no":detail_data[0],"name":detail_data[1],"subject":detail_data[2],"content":detail_data[3],"regdate":detail_data[4],"hit":detail_data[5]}
    return render(request,'total/board/detail.html',dd) #forward {"dd",dd}  dd

#수정 , 삭제 , 답변
def board_update_data(request):
    no=request.GET['no']
    u_data=models.board_updata_data(int(no))
    #no,name,subject,content
    ud={"no":u_data[0],"name":u_data[1],"subject":u_data[2],"content":u_data[3]}
    return render(request,'total/board/update.html',ud)
def board_update_ok(request):
    name=request.POST['name']
    subject=request.POST['subject']
    content=request.POST['content']
    pwd=request.POST['pwd']
    no=request.POST['no']
    udata=(no,name,subject,content,pwd)
    #데이터베이스 연동 결과값 => html
    result=models.board_update_ok(udata)
    print(f"result={result}")
    return render(request,'total/board/update_ok.html',{"result":result,"no":no})

#답변
def board_reply(request):
    no=request.GET['no']
    return render(request,'total/board/reply.html',{"no":no})

def board_reply_ok(request):
    pno=request.POST['pno']
    name = request.POST['name']
    subject = request.POST['subject']
    content = request.POST['content']
    pwd = request.POST['pwd']
    rdata=(pno,name,subject,content,pwd)
    #models연결 => 오라클 연결 => 추가
    models.board_reply(rdata)
    return redirect("/total/board/list/")

def board_delete(request):
     no=request.GET['no']
     return render(request,'total/board/delete.html',{"no":no})

def board_delete_ok(request):
     no=request.POST['no']
     pwd=request.POST['pwd']
     #데이터베이스로 전송
     result=models.board_delete(int(no),pwd)
     return render(request,'total/board/delete_ok.html',{"result":result})
















