from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pymysql

def academy(conn, cur, tablename, tablenewname, driver_path):

    wd = webdriver.Chrome(executable_path=driver_path)
    cur.execute("select * from "+tablename+";")
    select=list(cur.fetchall())
    conn.commit()

    academies=[]
    for sl in select:
        if sl[1] == '삼성서울병원':
            name=sl[0]
            belong=sl[1]
            #link=sl[len(sl)-1]
            link=sl[5]
            wd.get(link)
            time.sleep(1)
            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')
            atimes=[]
            anames=[]
            author=[]
            texts=[]
            tr=[]
            th=[]
            td=[]
            atime=''
            aname=''
            try:
                for table in soup.find_all('table',{'class','table-default table-type03'}):
                    if '학회활동'in table.text:
                        author=table
                for tr in author.find_all('tr'):
                    academy=[]
                    if tr.find('th')==None and tr.find('td')==None:
                        texts=th.text
                    elif tr.find('th')!=None:
                        th=tr.find('th')
                        texts=th.text
                        word1=''
                        atime=word1.join(word1.join(word1.join((texts.split('\t'))).split('\n')).split('\r'))
                    else:
                        atime=None
                    td=tr.find('td')
                    aname=td.text
                    atimes.append(atime)
                    anames.append(aname)
                    
                    academy.append(name)
                    academy.append(belong)
                    academy.append(aname)
                    academy.append(atime)
                    academies.append(academy)
            except:
                atimes=None
                anames=None
            
    wd.close()
    wd.quit()

    for i in academies:
        cur.execute("INSERT INTO "+tablenewname+" (name_kor, belong, academy, academy_period) VALUES (%s,%s,%s,%s);",(i[0],i[1],i[2],i[3]))
        conn.commit()
