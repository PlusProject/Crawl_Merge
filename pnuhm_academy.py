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

    ### 크롤링 코드 시작 ###
    BUSANURLLIST=["https://www.pnuh.or.kr/pnuh/treat/info.do?rbsIdx=116&code=I2&type=2","https://www.pnuh.or.kr/pnuh/treat/info.do?rbsIdx=116&code=TS&type=2"]

    for urlitem in BUSANURLLIST:
        time.sleep(2)
        wd.get(urlitem)
        year=None
        doctorlist=wd.find_elements_by_css_selector("div.btn > a:nth-child(1) > span")
        for i in range(len(doctorlist)):
            wd.get(urlitem)
            time.sleep(2)
            doctorlist = wd.find_elements_by_css_selector("div.btn > a:nth-child(1) > span")
            button=doctorlist[i]
            button.click()
            time.sleep(1)
            wd.switch_to.window(wd.window_handles[-1])
            time.sleep(1)

            # detail01
            name_kor=wd.find_element_by_css_selector("#contents_area > div.teamIntro_doctor > div.mTit > h2 > strong").text
            belong="부산대학교병원"
            hospital_code = "602720"
            anamelist = wd.find_elements_by_css_selector(
                "#contents_area > article > div:nth-child(2) > div > div:nth-child(7) > table > tbody > tr > td")
            for i in anamelist:
                if (i.text != ""):
                    aname = i.text
                    year = None

                    ### 정보들 테이블에 insert
                    cursor.execute("""insert into """+table_name+"""
                                                            (name_kor, belong, academy,academy_period)
                                                            values (%s, %s, %s, %s)
                                                            """, (name_kor, belong, aname, year))
                    connect.commit()


    wd.close()
    wd.quit()
