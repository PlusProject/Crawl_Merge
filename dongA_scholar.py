### import ###
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql

### 동아대학교병원  테이블 ###
def scholar(connect, cursor, table_name, driver_path):
    
    ### 크롬드라이버 생성 ###
    wd = webdriver.Chrome(executable_path=driver_path)
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
                pname = []
                for p, q in enumerate(txts):
                    data = q.text.split(maxsplit=1)

                    ### 논문 가져오기 ###
                    try:
                        if data[0] == "주요논문":
                            # 논문 데이터 전처리
                            pat1 = re.compile("[:]\d{4}[:]\d+[-]\d+")  #방정희
                            data[1] = pat1.sub("", data[1])
                            pat2 = re.compile("[;][\s]\d{4}[;]\d+[-]\d+")  #방정희
                            data[1] = pat2.sub("", data[1])
                            pat3 = re.compile("[:][\s]\d{4}[\s][:][\s]\d+[-]\d+") #조광조
                            data[1] = pat3.sub("", data[1])
                            pat4 = re.compile("[\s]\d{4}[;][\s]\d+[(]\d+[)][:][\s]\d+[-]\d+")  #맞음
                            data[1] = pat4.sub("", data[1])
                            pat5 = re.compile("[\s]\d{4}[;]\d+[:]\d+[-]\d+")    #맞음
                            data[1] = pat5.sub("", data[1])
                            pat6 = re.compile("[A-Za-z]+[;]\d+[(]\d+[)][:][a-z]\d+") #임경희에 영향
                            data[1] = pat6.sub("", data[1])
                            pat7 = re.compile("[\s]\d{4}[;]\d+[(]\d+[)][:]\d+[-]\d+") #맞음
                            data[1] = pat7.sub("", data[1])
                            pat8 = re.compile("[\s]\d+[:]\d+") #맞음
                            data[1] = pat8.sub("", data[1])
                            pat9 = re.compile("[\s]\d+[:]") #맞음
                            data[1] = pat9.sub("", data[1])
                            pat10 = re.compile("[\s][;][\s]\d+[-]\d+")  # 조광조
                            data[1] = pat10.sub("", data[1])
                            pat11 = re.compile("[\s][:][-]\d+")  # 조광조, 방정희
                            data[1] = pat11.sub("", data[1])
                            pat12 = re.compile("[\s][(]\d+[\s][A-Za-z]+[\s]\d+[)]")  # 정상석
                            data[1] = pat12.sub("", data[1])
                            pat13 = re.compile("[:][-]\d+")  # 정상석
                            data[1] = pat13.sub("", data[1])
                            pat14 = re.compile("[;]\d{4}[;]\d+[-]\d+")  # 방정희
                            data[1] = pat14.sub("", data[1])
                            pat15 = re.compile("[;][\s]\d{4}[;][\s]\d+[-]\d+")  # 방정희
                            data[1] = pat15.sub("", data[1])
                            pat16 = re.compile("[\s][:][\s]\d+[-]\d+")  # 정상석
                            data[1] = pat16.sub("", data[1])
                            pat17 = re.compile("[\n][;][-]\d+")  # 정상석
                            data[1] = pat17.sub("", data[1])
                            pat18 = re.compile("[;]\d+[-]\d+")  # 정상석
                            data[1] = pat18.sub("", data[1])
                            pat19 = re.compile("[\s][:][\s]\d+[;]\d+[)][:]\d+[-]\d+")  # 방정희
                            data[1] = pat19.sub("", data[1])
                            pat20 = re.compile("[;][-]\d+")  # 정상석
                            data[1] = pat20.sub("", data[1])
                            pat21 = re.compile("[\s][:]")  # 정상석
                            data[1] = pat21.sub("", data[1])
                            pat22 = re.compile("[:][\s]\d+[-]\d+")  # 정상석
                            data[1] = pat22.sub("", data[1])
                            pat23 = re.compile("[;]\d{4}")  # 맞음(맨 앞에 년도 지우기)
                            data[1] = pat23.sub("", data[1])
                            pat24 = re.compile("\d{4}[\s]")  # 맞음(맨 앞에 년도 지우기)
                            data[1] = pat24.sub("", data[1])
                            pat25 = re.compile("\d+[.][\s]")  # 맞음(맨 앞 논문 순서 번호 지우기)
                            data[1] = pat25.sub("", data[1])
                            data[1] = data[1].replace(' 2009 Dec;36(6):1006-10. doi:\n10.1016/j.ejcts.2009.05.048. Epub 2009 Jul 29.', '')  # 방정희
                            data[1] = data[1].replace('Kyungil Park, et al. ','')   # 박경일
                            data[1] = data[1].replace('※과학기술논문색인(SCI) 학술지 제 1저자', '')  # 박경일

                            data[1] = data[1].replace('\n\n', '\t')
                            if '\n' not in data[1]:
                                pname = data[1] + '\t'
                            else:
                                pname = data[1]
                            if '\t' in pname and '\n' in pname:
                                pname = pname.split('\t')
                            elif '\t' in pname and '\n' not in pname:
                                pname = pname.split('\t')
                            elif '\t' not in pname and '\n' in pname:
                                pname = pname.split('\n')

                            for i in range(0, len(pname)):
                                if pname[i] == '' or pname[i] == '\n':
                                    del pname[i]
                        ### 논문 수집안되었을 시 ###
                        if pname == []:
                            pname = ''  # 어차피 논문정보 없으면 테이블에 저장 안 함
                    except:
                        pass
                ### mysql insert ###
                for i in range(len(pname)):
                    cursor.execute("INSERT INTO " + table_name + "(name_kor, belong, pname)values (%s, %s, %s);", (name_kor, belong, pname[i]))

                wd.switch_to.default_content()
    connect.commit()
    
    wd.close()
    wd.quit()
