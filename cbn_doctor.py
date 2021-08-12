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
    url="https://www.cbnuh.or.kr/sub03/sub03_01.jsp"
    wd.get(url)

    #department=['심장내과','흉부외과']
    department = ['순환기내과', '심장내과', '심장외과', '흉부외과', '심장혈관외과', '소아심장과']
    departmentLink=[]
    doctordepartmentLink=[]
    doctorLink=[]

    ###한번에 커밋하기 위한 작업###
    name_kor=[]
    belong=[]
    major=[]
    education=[] #학력
    career=[] #경력
    link=[]
    careers=[]



    ###진료과 링크 담은 후 크롤링하기###
    for i in department:
        data=wd.find_elements_by_partial_link_text(i)
        for a in data:
            departmentLink.append(a.get_attribute("href"))
    for i in departmentLink:
        wd.get(i)
        time.sleep(1)
        buttons=wd.find_elements_by_partial_link_text("상세보기")
        for j in range(0,len(buttons)):
            doctordepartmentLink.append(buttons[j].get_attribute('href'))
        
    #print(len(doctordepartmentLink))

    j=0
    k=1
    s=0
    for i in doctordepartmentLink:
        wd.get(i)
        ###name_kor수집###
        name_kor.append(wd.find_element_by_xpath('//*[@id="content_area"]/div/div[1]/ul/li[1]'))
        name_kor[j]=name_kor[j].text
        #print(name_kor[j])
        ###belong수집: notion_대학병원이름에서 병원 명칭(홈페이지)이름으로 저장 ###
        belong="충북대학교병원"
        ###hospital_code수집: notion_대학병원이름에서 병원코드 저장 ###
        hospital_code ="361710"
        ###major수집###
        major.append(wd.find_element_by_xpath('//*[@id="content_area"]/div/div[2]/table/tbody/tr[1]/td'))
        major[j]=major[j].text
        #print(belong)
        #print(major[j])
        ###education,career수집(career에 저장함)-> 학력하고 경력이 같이 나와있음###
        education=wd.find_element_by_css_selector('#content_area > div > div.table_area > table > tbody > tr:nth-child(2) > td > dl > dd')
        career=education.text.split('\n\n')[0]
        career=career.split('\n')
        del career[0]
        career=",".join(career)
        #print('학력+경력:'+career)
        careers.append(career)
        ###link수집###
        link.append(wd.current_url)
        #print(link[j])
        
        j=j+1
        k=k+1


    for i in range(len(name_kor)):
        cursor.execute("insert into "+ table_name+"(name_kor, belong,major,education,career,link,hospital_code) values( %s,%s,%s,%s,%s,%s,%s);",(name_kor[i],belong, major[i],None,careers[i],link[i],hospital_code))
    connect.commit()
    
    wd.close()
    wd.quit()
