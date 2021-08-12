### import ###
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql

### 동아대학교병원 학회 테이블 ###
def academy(connect, cursor, table_name, driver_path):
    ### 크롬드라이버 생성 ###
    wd=webdriver.Chrome(executable_path=driver_path)

    ### 크롤링 코드 시작 ###
    department = ["순환기내과", "심장내과", "심장외과", "흉부외과", "심장혈관외과", "소아심장과"]
    dongAURL = "https://www.damc.or.kr/02/02_2017.php"
    wd.get(dongAURL)
    # 진료과 링크 담기
    departmentLink = []
    names = wd.find_elements_by_class_name('depart_box.left')
    size = len(names)
    for m in range(0, size):
        name = names[m].find_element_by_tag_name('h4').text
        if name in department:
            options = names[m].find_elements_by_tag_name('a')
            departmentLink.append(options[1].get_attribute('href'))
    # 의료진 페이지 담기
    for n in departmentLink:
        wd.get(n)
        page = wd.find_element_by_class_name('paging')
        pages = page.find_elements_by_tag_name('a')
        del pages[0]  # 이전페이지 버튼 제거
        del pages[-1]  # 다음페이지 버튼 제거
        for i, j in enumerate(pages):  # 페이지 돌기(2페이지 -> 0, 1)
            if i != 0:
                j.send_keys(Keys.ENTER)
            time.sleep(1)
            lst = wd.find_elements_by_link_text("의료진 소개")
            del lst[0]  # 제목에 있는 '의료진 소개' 버튼 제거
            for index, k in enumerate(lst):
                k.send_keys(Keys.ENTER)  # 각 의료진의 '의료진 소개' 버튼 누르기
                time.sleep(5)
                pop_up = wd.find_element_by_tag_name('iframe')
                wd.switch_to.frame(pop_up)

                ### name_kor 수집 ###
                name_kor = wd.find_element_by_class_name('docLeft').text
                ### belong 수집: notion_대학병원이름에서 병원 명칭(홈페이지)이름으로 저장 ###
                belong = "동아대학교병원"

                txts = wd.find_elements_by_css_selector("div.docDetail > div.docRight > table > tbody > tr")
                academy = []
                academy_period = []
                for p, q in enumerate(txts):
                    data = q.text.split(maxsplit=1)

                    ### 학회/년도 정보 수집 ###
                    try:
                        ### 학회 정보 수집 ###
                        if data[0] == "학회활동":
                            academy = data[1]
                            academy = academy.split('\n')
                            ### academy_period 정보 수집 ###
                            p1 = re.compile('\d{4}[-]\d{4}')
                            p2 = re.compile('\d{4}')
                            for i in range(0, len(academy)):
                                m = p1.search(academy[i])
                                n = p2.search(academy[i])
                                if m:
                                    academy_period.append(m.group())
                                elif n:
                                    academy_period.append(n.group())
                                else:
                                    academy_period.append(None)
                            ### academy_period 수집안되었을 시 ###
                            if academy_period == []:
                                academy_period = None
                        ### 학회 수집안되었을 시 ###
                        if academy == []:
                            academy = ""  # 어차피 학회정보 없으면 테이블에 저장 안 함
                    except:
                        pass
                ### mysql insert ###
                for i in range(len(academy)):
                    cursor.execute("INSERT INTO " + table_name + "(name_kor, belong, academy, academy_period)values (%s, %s, %s, %s);", (name_kor, belong, academy[i], academy_period[i]))

                wd.switch_to.default_content()
    connect.commit()

    wd.close()
    wd.quit()
