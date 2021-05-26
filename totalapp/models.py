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
    print(movie_data)
    cursor.close()
    conn.close()
    return movie_data

movie_list(1)


