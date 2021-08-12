from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import pymysql

def scholar(conn, cur, tablename, tablenewname, driver_path):

    wd = webdriver.Chrome(executable_path=driver_path)
    cur= conn.cursor()
    cur.execute("select * from "+tablename+";")
    select=list(cur.fetchall())
    conn.commit()

    pubs=[]
    for sl in select:
        if sl[1] == '삼성서울병원':
            name=sl[0]
            belong=sl[1]

            #link=sl[len(sl)-1]
            link=sl[5]
            wd.get(link)
            time.sleep(1)
            html = wd.current_url
            soup = BeautifulSoup(html, 'html.parser')
            publication=[]
            try:
                wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                wd.find_element_by_link_text('논문').click()
                time.sleep(1)
                html = urlopen(wd.current_url)
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    while 1:
                        elm=wd.find_element_by_css_selector('#doctor-paper-section03 > div > div > div.paper-list-body > div > div.more-view2 > button')
                        elm.click()
                except:
                    html=wd.page_source
                    soup=BeautifulSoup(html,'html.parser')
                    for p in soup.find_all('strong',{'class','paper-name'}):
                        publication.append(p.text)
                    count=len(publication)
            except:
                publication='null'
                count=0
            if publication!='null':
                for pname in publication:
                    pub=[]
                    pub.append(name)
                    pub.append(belong)
                    pub.append(pname)
                    pubs.append(pub)

    wd.close()
    wd.quit()

    for i in pubs:
        cur.execute("INSERT INTO "+tablenewname+" (name_kor, belong, pname) VALUES (%s,%s,%s);",(i[0],i[1],i[2]))
        conn.commit()
