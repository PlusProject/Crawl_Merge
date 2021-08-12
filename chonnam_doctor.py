### import ###
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql


def doctor(connect, cursor, table_name, driver_path):

    ### 크롬드라이버 생성 ###
    wd=webdriver.Chrome(executable_path=driver_path)

    ### 크롤링 코드 시작 ###
    CHONNAMURLLIST=["http://www.cnuh.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=CV","http://www.cnuh.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=CS","https://www.cnuhch.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=PECV"]
    for urlitem in CHONNAMURLLIST:
        time.sleep(2)
        wd.get(urlitem)
        doctorlist=wd.find_elements_by_css_selector("#contents > div.sectionArea > ul > li > div > div.doctor > dl > dd.lkList > ul > li.intro > a > span")
        for i in range(len(doctorlist)):
            wd.get(urlitem)
            time.sleep(2)
            doctorlist = wd.find_elements_by_css_selector("#contents > div.sectionArea > ul > li > div > div.doctor > dl > dd.lkList > ul > li.intro > a > span")
            button=doctorlist[i]
            button.click()
            time.sleep(2)

            ### name_kor 수집 ###
            name_kor=wd.find_element_by_css_selector("#contents > div.doctorIntro > div.introHeader > div > dl > dt").text
            belong="전남대학교병원"
            hospital_code = "501710"
            major=wd.find_element_by_css_selector("#contents > div.doctorIntro > div.introHeader > div > dl > dd").text[4:]
            education =""
            educationlist=wd.find_elements_by_css_selector("#introDetail01 > div:nth-child(1) > dl > dd> span.txt")
            for i in educationlist:
                if(i.text!=""):
                    education=education+i.text+","
            if (education == ""):
                education = None
            career=""
            try:
                button=wd.find_element_by_css_selector("#introDetail01 > div:nth-child(2) > p > button")
                button.click()
            except:
                continue
            time.sleep(1)
            careerlist=wd.find_elements_by_css_selector("#introDetail01 > div:nth-child(2) > dl > dd > span.txt")
            for j in careerlist:
                if (j.text!=""):
                    career=career+j.text+","
            if (career == ""):
                career = None
            link=wd.current_url

            ### mysql insert ###
            cursor.execute(
                "INSERT INTO " + table_name + "(name_kor, belong, major, education, career, link, hospital_code) values (%s, %s, %s, %s, %s, %s, %s);",
                (name_kor, belong, major, education, career, link, hospital_code))
            connect.commit()

    wd.close()
    wd.quit()

