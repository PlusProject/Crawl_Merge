### import ###
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql
from selenium.common.exceptions import NoSuchElementException

### 연세대학교원주세브란스기독병원 학회 테이블 ###
def academy(connect, cursor, table_name, driver_path):
    ### 크롬드라이버 생성 ###
    wd = webdriver.Chrome(executable_path=driver_path)

    ### 크롤링 코드 시작 ###
    department = ['순환기내과', '심장내과', '심장외과', '흉부외과', '심장혈관외과', '소아심장과']
    departmentLink = []
    doctocdepartmentLink = []
    doctorLink = []

    severanceWonjuURL = 'https://www.ywmc.or.kr/web/www/medical_office'
    wd.get(severanceWonjuURL)

    contents = wd.find_element_by_class_name('content')
    for i in department:
        data = contents.find_elements_by_partial_link_text(i)
        for a in data:
            departmentLink.append(a.get_attribute("href"))

    for i in departmentLink:
        wd.get(i)
        options = wd.find_elements_by_tag_name('a')
        for i in options:
            if ('의료진' == i.text):
                doctocdepartmentLink.append(i.get_attribute('href'))

    for i in doctocdepartmentLink:
        wd.get(i)
        doclist = wd.find_elements_by_css_selector('div.doct_list > div.d_bx > div.d_info')
        for index, value in enumerate(doclist):
            major = None
            education = None
            career = None
            link = None
            namelist = value.find_element_by_class_name('name').text
            if namelist != '일반진료':
                ### name_kor 수집 ###
                name_kor = namelist
                ### belong 수집: notion_대학병원이름에서 병원 명칭(홈페이지)이름으로 저장 ###
                belong = "연세대학교원주세브란스기독병원"

                academy = []
                academy_period = []
                link = wd.current_url
                raw = requests.get(link)
                html = BeautifulSoup(raw.text, "html.parser")
                # 학력box인지 학회box인지 고르는 부분
                ls = html.select(('#_doctorView_WAR_reservportlet_pop_rsv_cplt-%s > div > div.pop_cont > div.portfolio > div' % index))
                for lst in ls:
                    op = lst.select_one('p').text
                    ### academy 수집 ###
                    try:
                        if op == '학술활동':
                            a = lst.select('ul > li')
                            academy.append(str(a))
                            academy = "".join(academy)
                            specialChars = "[]"
                            for specialChar in specialChars:
                                academy = academy.replace(specialChar, '')
                            academy = academy.replace('<li>','')
                            academy = academy.replace('</li>', '')
                            academy = academy.split('<br/>')    #리스트에 넣기
                            ### academy_period 수집 ###
                            for j in academy:
                                pat = re.compile('\d{4}[.]\d+[-]\d{4}[.]\d+|\d{4}[.]\d+[-][현][재]|\d{4}[-][현][재]|\d{4}[~]\d{4}|\d{4}\s[~]\s')
                                match = pat.search(j)
                                if match == None:
                                    match = '0'
                                else:
                                    match = match.group()
                                academy_period.append(match)
                    except:
                        academy = ''

                for k in range(0,len(academy)):
                    if academy_period[k] in academy[k]:
                        academy[k] = academy[k].replace(academy_period[k], '')
                    academy[k] = academy[k].replace('()', '')

                if academy == []:
                    academy = ''
                if academy_period == []:
                    academy_period = None
                else:
                    for i, j in enumerate(academy_period):
                        if j == '0':
                            academy_period[i] = None

                ### mysql insert ###
                for i in range(len(academy)):
                    cursor.execute(
                        "INSERT INTO " + table_name + "(name_kor, belong, academy, academy_period)values (%s, %s, %s, %s);",
                        (name_kor, belong, academy[i], academy_period[i]))

    connect.commit()
    
    wd.close()
    wd.quit()
