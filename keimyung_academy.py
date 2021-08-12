### import ###
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql

### 계명대학교동산병원 학회 테이블 ###
def academy(connect, cursor, table_name, driver_path):
    ### 크롬드라이버 생성 ###
    wd = webdriver.Chrome(executable_path=driver_path)
    ### 크롤링 코드 시작 ###
    department = ['순환기내과', '심장내과', '심장외과', '흉부외과', '심장혈관외과', '소아심장과']
    departmentLink = []
    doctorLink = []

    keimyungURL = 'http://dongsan.dsmc.or.kr/content/02health/01_01.php'
    wd.get(keimyungURL)
    # 진료과 링크 담기
    for i in department:
        data = wd.find_elements_by_partial_link_text(i)
        for a in data:
            departmentLink.append(a.get_attribute("href"))
    # 의료진 페이지 담기
    for i in departmentLink:
        wd.get(i)
        options = wd.find_elements_by_tag_name('a')
        for i in options:
            if ('의료진소개' in i.text):
                doctorLink.append(i.get_attribute('href'))
    # 각 의료진 페이지
    for doctor in doctorLink:
        academy = []
        academy_period = []

        wd.get(doctor)
        time.sleep(2)
        text = wd.find_element_by_css_selector('div.treat_doc_tit > p.btxt').text
        ### name_kor 수집 ###
        name_kor = text[0:len(text) - 3]
        ### belong 수집: notion_대학병원이름에서 병원 명칭(홈페이지)이름으로 저장 ###
        belong = "계명대학교동산병원"

        ### 학회/년도 정보 수집 ###
        ls = wd.find_elements_by_css_selector('body > div.doc_cont > div.box1')
        for lst in ls:
            op = lst.find_element_by_tag_name('h3').text
            if op == '학회활동':
                li = lst.find_elements_by_css_selector('table > tbody > tr')
                for list in li:
                    yr = list.find_element_by_tag_name('th').text
                    an = list.find_element_by_tag_name('td').text
                    if yr == '-' or yr == '-  ':
                        yr = None
                    academy.append(an)
                    academy_period.append(yr)
        if academy == []:
            academy = ''
        if academy_period == []:
            academy_period = None

        ### mysql insert ###
        for i in range(len(academy)):
            cursor.execute(
                "INSERT INTO " + table_name + "(name_kor, belong, academy, academy_period)values (%s, %s, %s, %s);",
                (name_kor, belong, academy[i], academy_period[i]))

        wd.switch_to.default_content()
    connect.commit()

    wd.close()
    wd.quit()
    
