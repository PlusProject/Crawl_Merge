### import ###
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql

def academy(connect, cursor, table_name, driver_path):
    ### 크롬드라이버 생성 ###
    wd=webdriver.Chrome(executable_path=driver_path)

    CHONNAMURLLIST=["http://www.cnuh.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=CV","http://www.cnuh.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=CS","https://www.cnuhch.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=PECV"]
    for urlitem in CHONNAMURLLIST:
        time.sleep(2)
        wd.get(urlitem)
        doctorlist=wd.find_elements_by_css_selector("#contents > div.sectionArea > ul > li > div > div.doctor > dl > dd.lkList > ul > li.intro > a > span")

        for i in range(len(doctorlist)):
            try:
                wd.get(urlitem)
                time.sleep(2)
                doctorlist = wd.find_elements_by_css_selector("#contents > div.sectionArea > ul > li > div > div.doctor > dl > dd.lkList > ul > li.intro > a > span")
                button=doctorlist[i]
                button.click()
                time.sleep(2)

                name_kor=wd.find_element_by_css_selector("#contents > div.doctorIntro > div.introHeader > div > dl > dt").text
                belong="전남대학교병원"
                link=wd.current_url

                raw = requests.get(link)
                html = BeautifulSoup(raw.text, "html.parser")
                # detail03
                # 학회 경력 순회
                aname=None
                year=None
                anamelist=html.select("#introDetail03 > div > dl > dd > span")
                for k in anamelist:
                    temp = k.text.strip()
                    if (temp!=''):
                        aname=temp

                        ### 정보들 테이블에 insert
                        cursor.execute("""insert into """ + table_name + """
                                                                                    (name_kor, belong, academy,academy_period)
                                                                                    values (%s, %s, %s, %s)
                                                                                    """,
                                       (name_kor, belong, aname, year))
                        connect.commit()
            except:
                pass




    wd.close()
    wd.quit()
