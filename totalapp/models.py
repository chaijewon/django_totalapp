from django.db import models
import cx_Oracle
"""
NO           NUMBER(3)     
CNO          NUMBER(1)     
TITLE        VARCHAR2(300) 
SINGER       VARCHAR2(200) 
ALBUM        VARCHAR2(200) 
POSTER       VARCHAR2(260) 
STATE        CHAR(6)       
IDCREMENT    NUMBER(3) 
"""
# Create your models here.
def getConnection():
    try:
          conn=cx_Oracle.connect("hr/happy@localhost:1521/xe")
    except Exception as e:
          print(e)
    return conn

def music_list(page):
    conn=getConnection()
    cursor=conn.cursor()
    rowSize=50
    start=(rowSize*page)-(rowSize-1)
    end=rowSize*page
    sql=f"""
            SELECT no,title,singer,album,poster,state,idcrement,num
            FROM (SELECT no,title,singer,album,poster,state,idcrement,rownum as num
            FROM (SELECT no,title,singer,album,poster,state,idcrement
            FROM genie_music ORDER BY no ASC))
            WHERE num BETWEEN {start} AND {end}
          """
    cursor.execute(sql)
    music_data=cursor.fetchall()
    print(music_data)
    cursor.close()
    conn.close()
    return music_data

def movie_list(page):
    conn=getConnection()
    cursor=conn.cursor()
    rowSize = 12
    start = (rowSize * page) - (rowSize - 1)
    end = rowSize * page
    sql = f"""
                SELECT mno,poster,title,num
                FROM (SELECT mno,poster,title,rownum as num
                FROM (SELECT /*+ INDEX_ASC(daum_movie dm_mno_pk) */ mno,poster,title
                FROM daum_movie))
                WHERE num BETWEEN {start} AND {end}
              """
    cursor.execute(sql)
    movie_data = cursor.fetchall()
    #print(movie_data)
    cursor.close()
    conn.close()
    return movie_data

def movie_totalpage():
    conn=getConnection()
    cursor=conn.cursor()
    sql="SELECT CEIL(COUNT(*)/12.0) FROM daum_movie"
    cursor.execute(sql)
    total=cursor.fetchone()
    cursor.close()
    conn.close()
    return total[0]
#movie_list(1)
'''
    NO     NOT NULL NUMBER         
    POSTER NOT NULL VARCHAR2(260)  
    TITLE  NOT NULL VARCHAR2(1000) 
    CHEF   NOT NULL VARCHAR2(200)  
    HIT             VARCHAR2(100)  
    LINK            VARCHAR2(100) 
'''
def recipe(page):
    conn=getConnection()
    cursor=conn.cursor()
    rowSize=8
    start=(rowSize*page)-(rowSize-1)
    end=rowSize*page
    sql=f"""
             SELECT no,poster,title,chef,num
             FROM (SELECT no,poster,title,chef,rownum as num
             FROM (SELECT /*+ INDEX_ASC(recipe recipe_no_pk) */ no,poster,title,chef
             FROM recipe))
             WHERE num BETWEEN {start} AND {end}
          """
    cursor.execute(sql)
    recipe_data=cursor.fetchall()
    cursor.close()
    conn.close()
    return recipe_data

def recipe_totalpage():
    conn=getConnection()
    cursor=conn.cursor()
    sql="SELECT CEIL(COUNT(*)/12.0) FROM recipe"
    cursor.execute(sql)
    total=cursor.fetchone() #(100,)
    print(total[0])
    cursor.close()
    conn.close()
    return total[0]

def recipe_count():
    conn=getConnection()
    cursor=conn.cursor()
    sql="SELECT COUNT(*) FROM recipe"
    cursor.execute(sql)
    count=cursor.fetchone()
    cursor.close()
    conn.close()
    return count[0]

def chef_totalpage(chef_name):
    conn=getConnection()
    cursor=conn.cursor()
    sql="SELECT CEIL(COUNT(*)/8.0) FROM recipe WHERE chef='"+chef_name+"'"
    print(sql)
    cursor.execute(sql)
    total=cursor.fetchone()
    #print(total)
    #print(total[0])
    cursor.close()
    conn.close()
    return total[0]

def chef_count(chef_name):
    conn = getConnection()
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM recipe WHERE chef='" + chef_name + "'"
    #print(sql)
    cursor.execute(sql)
    count = cursor.fetchone()
    # print(total)
    #print(count[0])
    cursor.close()
    conn.close()
    return count[0]

def chef_list(chef_name,page):
    conn = getConnection()
    cursor = conn.cursor()
    rowSize = 8
    start = (rowSize * page) - (rowSize - 1)
    end = rowSize * page
    sql = f"""
                 SELECT no,poster,title,chef,num
                 FROM (SELECT no,poster,title,chef,rownum as num
                 FROM (SELECT /*+ INDEX_ASC(recipe recipe_no_pk) */ no,poster,title,chef
                 FROM recipe WHERE chef='{chef_name}'))
                 WHERE num BETWEEN {start} AND {end}
              """
    print(sql)
    cursor.execute(sql)
    recipe_data = cursor.fetchall()
    #print(recipe_data)
    cursor.close()
    conn.close()
    return recipe_data
'''
RNO                  NUMBER         
POSTER      NOT NULL VARCHAR2(260)  
CHEF        NOT NULL VARCHAR2(200)  
CHEF_POSTER NOT NULL VARCHAR2(260)  
TITLE       NOT NULL VARCHAR2(2000) 
CONTENT     NOT NULL VARCHAR2(4000) 
INFO1       NOT NULL VARCHAR2(20)   
INFO2       NOT NULL VARCHAR2(20)   
INFO3       NOT NULL VARCHAR2(20)   
FOOD_MAKE   NOT NULL CLOB           
CHEF_INFO   NOT NULL VARCHAR2(1000)
'''
def recipe_detail(no):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
             SELECT poster,chef,chef_poster,title,content,info1,info2,info3,food_make,chef_info
             FROM recipe_make
             WHERE rno={no}
          """
    cursor.execute(sql)
    data=cursor.fetchone()
    chef_data=(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8].read(),data[9])
    cursor.close()
    conn.close()
    return chef_data
'''
MNO        NOT NULL NUMBER        
CNO                 NUMBER        
POSTER     NOT NULL VARCHAR2(260) 
TITLE      NOT NULL VARCHAR2(200) 
REGDATE             VARCHAR2(200) 
GENRE      NOT NULL VARCHAR2(100) 
NATION     NOT NULL VARCHAR2(50)  
GRADE      NOT NULL VARCHAR2(50)  
TIME       NOT NULL VARCHAR2(50)  
SCORE               NUMBER(2,1)   
SHOWUSER            VARCHAR2(30)  
BOXOFFICE           VARCHAR2(10)  
STORY               CLOB          
KEY                 VARCHAR2(30)  
REPLYCOUNT          NUMBER
'''
def movie_detail(mno):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
            UPDATE daum_movie SET
            replycount=replycount+1
            WHERE mno={mno}
          """
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    sql=f"""
            SELECT mno,poster,title,regdate,genre,nation,grade,time,score,showuser,boxoffice,story,key
            FROM daum_movie
            WHERE mno={mno}
          """

    cursor=conn.cursor()
    cursor.execute(sql)
    md=cursor.fetchone()
    print(md)
    movie_data=(md[0],md[1],md[2],md[3],md[4],md[5],md[6],md[7],md[8],md[9],md[10],md[11].read(),md[12])
    cursor.close()
    conn.close()
    return movie_data
# java => 데이터형 문자열 변환 (String.valueOf() == str())
#chef_totalpage('만개의레시피')
#chef_count('만개의레시피')
#chef_list('만개의레시피',1)
# 맛집관련
'''
NO      NOT NULL NUMBER        
TITLE   NOT NULL VARCHAR2(100) 
SUBJECT NOT NULL VARCHAR2(100) 
POSTER  NOT NULL VARCHAR2(260) 
'''
# md[11].read() 오라클의 데이터형이 clob
def food_category(start,end):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
            SELECT no,title,subject,poster 
            FROM food_category
            WHERE no BETWEEN {start} AND {end}
          """
    cursor.execute(sql)
    food_data=cursor.fetchall()
    cursor.close()
    conn.close()
    return food_data


'''
NO      NOT NULL NUMBER         
CNO              NUMBER         
POSTER  NOT NULL VARCHAR2(4000) 
TITLE   NOT NULL VARCHAR2(200)  
SCORE   NOT NULL NUMBER(2,1)    
ADDRESS NOT NULL VARCHAR2(300)  
TEL     NOT NULL VARCHAR2(30)   
TYPE    NOT NULL VARCHAR2(100)  
PRICE   NOT NULL VARCHAR2(50)   
PARKING          VARCHAR2(500)  
TIME             VARCHAR2(500)  
MENU             VARCHAR2(2000) 
GOOD             NUMBER         
SOSO             NUMBER         
BAD              NUMBER        
'''
# Object_all()
def food_list(cno):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
            SELECT no,poster,title,address,tel
            FROM food_house
            WHERE cno={cno}
          """
    cursor.execute(sql)
    food_data=cursor.fetchall()
    cursor.close()
    conn.close()
    return food_data

def food_detail(no):
    conn=getConnection()
    cursor=conn.cursor()
    sql=f"""
             SELECT poster,title,score,address,tel,type,price,parking,time,menu,good,soso,bad
             FROM food_house
             WHERE no={no}
          """
    cursor.execute(sql)
    detail_data=cursor.fetchone()
    cursor.close()
    conn.close()
    return detail_data




