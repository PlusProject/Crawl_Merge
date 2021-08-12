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

    # 충남대학교
    # 버튼: #con_section_day > div > ul > li > div > div.photos > a > span

    CNULIST=["https://www.cnuh.co.kr/prog/cnuhTreatment/home/view.do?gwaCode=IM1&mno=sub01_0101&tabGubun=tab2","https://www.cnuh.co.kr/prog/cnuhTreatment/home/view.do?gwaCode=CS&mno=sub01_0101&tabGubun=tab2"]
    for urlitem in CNULIST:
        time.sleep(2)
        wd.switch_to.window(wd.window_handles[0])
        wd.get(urlitem)
        doctorlist=wd.find_elements_by_css_selector("#con_section_day > div > ul > li > div > div.photos > a > span")
        for i in range(len(doctorlist)):
            time.sleep(1)
            wd.switch_to.window(wd.window_handles[0])
            time.sleep(2)
            doctorlist=wd.find_elements_by_css_selector("#con_section_day > div > ul > li > div > div.photos > a > span")
            knamelist = wd.find_elements_by_css_selector("#con_section_day > div > ul > li > div > strong")
            name_kor=knamelist[i].text.split(" ")[0]
            hospital_code="301730"
            majorlist=wd.find_elements_by_css_selector("#con_section_day > div > ul > li > div > p:nth-child(3)")
            major=majorlist[i].text
            try:
                button=doctorlist[i]
                button.click()
                time.sleep(2)
                wd.switch_to.window(wd.window_handles[-1])
                time.sleep(1)

                # detail01
                belong = "충남대학교병원"
                aname = None
                year = None
                anamelist = wd.find_elements_by_css_selector(
                    "#body_layout > div.linebox.step_1 > div > ul > li:nth-child(2) > div > div:nth-child(1) > ul > li")

                wd.close()

                for i in anamelist:
                    if (i.text != ""):
                        aname = i.text
                        year = None
                        
                        ### 정보들 테이블에 insert
                        cursor.execute("""insert into """+table_name+"""
                                        (name_kor, belong, academy,academy_period)
                                        values (%s, %s, %s, %s)""",(name_kor, belong, aname, year))
                        connect.commit()

            except:
                pass

    
    wd.quit()

