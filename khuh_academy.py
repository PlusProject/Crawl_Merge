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
    # kname, belong, major, education, career, link
    KHUNGHEELIST=["https://www.khuh.or.kr/03/01_06.php?section=6","https://www.khuh.or.kr/03/01_29.php?section=29"]
    for urlitem in KHUNGHEELIST:
        wd.get(urlitem)
        list = wd.find_elements_by_css_selector("table > tbody > tr:nth-child(14) > td > table > tbody > tr > td > table > tbody > tr > td > table > tbody > tr")
        for i in range(4, (len(list) - 1), 3):
            info=list[i]
            # detail01
            name_kor=info.find_element_by_css_selector("td:nth-child(2) > b").text
            belong="경희대학교병원"
            aname=None
            year=None
            temp=info.find_element_by_css_selector("td:nth-child(4) > font > table > tbody > tr:nth-child(9) > td:nth-child(2)").text
            templist=temp.split("\n")
            for i in templist:
                aname=i
                
                ### 정보들 테이블에 insert
                cursor.execute("""insert into """ + table_name + """
                                                                            (name_kor, belong, academy,academy_period)
                                                                            values (%s, %s, %s, %s)
                                                                            """, (name_kor, belong, aname, year))
                connect.commit()

    wd.close()
    wd.quit()



