### import ###
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql

### 계명대학교동산병원 논문 테이블 ###
def scholar(connect, cursor, table_name, driver_path):
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
        pname = []
        wd.get(doctor)
        time.sleep(2)
        text = wd.find_element_by_css_selector('div.treat_doc_tit > p.btxt').text
        ### name_kor 수집 ###
        name_kor = text[0:len(text) - 3]
        ### belong 수집: notion_대학병원이름에서 병원 명칭(홈페이지)이름으로 저장 ###
        belong = "계명대학교동산병원"

        ### 논문 가져오기 ###
        try:
            option = wd.find_element_by_link_text('논문')
            option.click()
            lst = wd.find_elements_by_css_selector('body > div.doc_cont > div > ul > li')
            count = len(lst)
            if count > 0:   # 논문이 list로 표현
                for list in lst:
                    if '\n' in list.text:
                        tmp = list.text.split('\n')
                        temp = tmp[1]
                    else:
                        temp = list.text

                    # 불규칙적으로 붙어있는 텍스트(전처리 불가)
                    temp = temp.replace('이정민, 허승호, 남창욱, 한성욱, 김기식, 김윤년, 김권배, ', '')
                    temp = temp.replace('김미경, 허승호, 이영수, 한성욱, 김윤년, 김기식, 김권배, ', '')
                    temp = temp.replace('김권배, 최세영,김재현,박창권,이광숙,유영선,이인규,김기식,김윤년, 한승세, ', '')
                    temp = temp.replace(
                        'Weon Kim, Myung-Ho Jeong, Kwang-Soo Cha, Dae-Woo Hyun, Seung-Ho Hur, Kwon-Bae Kim, Young-Joon Hong, Hyung-Wook Park, Ju-Han Kim, Young-Keun Ahn, Moo-Hyun Kim, Jeong-Gwan Cho, Jong-Tae Park, Jong-Chun Park, Jung-Chaee Kang, ',
                        '')
                    temp = temp.replace(
                        'Kwon-Bae Kim, Seung-Jung Park, Seong-Wook Park, Jae-Joong Kim, Myeong-Ki Hong Cheol-Whan Lee, Young-Moo Ro, Jung-Chaee Kang, Young-Jo Kim, Byung-Hee Oh, Won-Ro Lee, Chong-Yun Rim, Jae-Eun Jun, Seung-Yun Cho, Kyu-Bo Choi, ',
                        '')
                    temp = temp.replace(
                        'Kim U, Kim DK, Seol SH, Yang TH, Kim DK, Kim DI, Kim DS, Lee SH, Hong GR, Park JS, Shin DG, Kim YJ, Cho YK, Kim HS, Nam CW, Hur SH, Kim KB,',
                        '')
                    temp = temp.replace(' J Echocardiogr. 2019 Mar 27. doi: 10.1007/s12574-019-00427-y.', '')
                    temp = temp.replace(' Ultrasound Med Biol. 2018 Jul 3. pii: S0301-5629(18)30218-7. doi: 10.1016/j.ultrasmedbio.2018.05.015. [Epub ahead of print]', '')
                    temp = temp.replace(' Am J Cardiol. 2018 Mar 2. pii: S0002-9149(18)30249-2.', '')
                    temp = temp.replace(' J Atheroscler Thromb. 2017 Jul 21. doi: 10.5551/jat.40469. [Epub ahead of print]', '')
                    temp = temp.replace(' J Am Heart Assoc. 2017 Feb 14;6(2). pii: e005424.', '')
                    temp = temp.replace(' PLoS One. 2018 Dec 7;13(12):e0208734.', '')
                    temp = temp.replace(' Circ Cardiovasc Imaging. 2018 Mar;11(3):e006986', '')
                    #temp = temp.replace(' PLoS One. 2018 Dec 7;13(12):e0208734.', '')

                    # 데이터 전처리
                    pat1 = re.compile("[,][\s]\d{4}[-]\d+[-]\d+")
                    temp = pat1.sub("", temp)
                    pat2 = re.compile("[,][\s]\d+[-]\d+")
                    temp = pat2.sub("", temp)
                    pat3 = re.compile("[,][\s][제]\d+[권][\s]\d+[호]")
                    temp = pat3.sub("", temp)
                    pat4 = re.compile("[,][\s]\d+[권][\s]\d+[호]")
                    temp = pat4.sub("", temp)
                    pat5 = re.compile("[,][\s]\d+[권]\d+[호]")
                    temp = pat5.sub("", temp)
                    pat6 = re.compile("[,][\s][제]\d+[권][제]\d+[호]")
                    temp = pat6.sub("", temp)
                    pat7 = re.compile("[,][\s][제]\d+[권][\s][제]\d+[호]")
                    temp = pat7.sub("", temp)
                    pat8 = re.compile("[,][\s]\d+[-]\d+")
                    temp = pat8.sub("", temp)
                    pat9 = re.compile("[,][\s]\d+[(]\d+[)]")
                    temp = pat9.sub("", temp)
                    pat10 = re.compile("[,][\s]\d+[~]\d+")
                    temp = pat10.sub("", temp)
                    pat11 = re.compile("[\s]\d{4}[\s][A-Za-z]+[\s]\d+[;]")
                    temp = pat11.sub("", temp)
                    pat12 = re.compile("[\s]\d{4}[\s][A-Za-z]+[;]")
                    temp = pat12.sub("", temp)
                    pat13 = re.compile("\d+[(]\d+[)][:]\d+[-]\d+[.]")
                    temp = pat13.sub("", temp)
                    pat14 = re.compile("\d+[:]\d+[-]\d+[.]")
                    temp = pat14.sub("", temp)
                    pat15 = re.compile("[\s]\d{4}[;]")
                    temp = pat15.sub("", temp)
                    pat16 = re.compile("[,][\s]\d+")
                    temp = pat16.sub("", temp)
                    temp = re.sub(r' \([^)]*\)', '', temp) #김재현

                    temp = temp.replace(', ,', ',')
                    temp = temp.replace(', 대학논문집', '')
                    temp = temp.replace(', 전국규모전문학술지', '')
                    temp = temp.replace(', 국제전문학술지', '')
                    temp = temp.replace(', 대한내과학회지', '')
                    temp = temp.replace(', 순환기', '')
                    temp = temp.replace(', 한국심초음파학회지', '')
                    temp = temp.replace(', 한국심초음파 학회지', '')
                    temp = temp.replace(', 계명의대 논문집', '')
                    temp = temp.replace(', 국외전문학술지', '')
                    temp = temp.replace(', 대한소화기학회지', '')
                    temp = temp.replace(', 예방의학회지', '')
                    temp = temp.replace(', 대한흉부외과학회지', '')
                    temp = temp.replace(', 기타논문집', '')
                    temp = temp.replace(', 계명대학 논문집', '')
                    temp = temp.replace(', 계명대논문집', '')
                    temp = temp.replace(', 계명대학교 논문집', '')
                    temp = temp.replace(', 계명의대학술지', '')

                    pname.append(temp)

            else:   # 논문이 table로 표현
                lst = wd.find_elements_by_css_selector('body > div.doc_cont > div > table > tbody > tr')
                for p, q in enumerate(lst):
                    data = q.text.split(maxsplit=1)
                    if data[0] == '제목':
                        pname.append(data[1])

        except:
            pass
        if pname == []:
            pname = ''  # 어차피 논문정보 없으면 테이블에 저장 안 함

        ### mysql insert ###
        for i in range(len(pname)):
            cursor.execute(
                "INSERT INTO " + table_name + "(name_kor, belong, pname) values (%s, %s, %s);",
                (name_kor, belong, pname[i]))

        wd.switch_to.default_content()

    connect.commit()

    wd.close()
    wd.quit()
