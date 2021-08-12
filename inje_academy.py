#인제대학교병원
#서울 : http://www.paik.ac.kr/seoul/treatment/search.asp
#부산 : http://www.paik.ac.kr/busan/treatment/search.asp
#상계 : http://www.paik.ac.kr/sanggye/treatment/search.asp
#일산 : http://www.paik.ac.kr/ilsan/treatment/search.asp
#해운대 : http://www.paik.ac.kr/haeundae/treatment/search.asp

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pymysql


def academy(conn, cursor, new_table, doctor_table, driver_path):
    
    main_url_front = 'http://www.paik.ac.kr/'
    main_url_back = '/treatment/search.asp'
    page_list = ['seoul', 'sanggye', 'ilsan', 'busan', 'haeundae']
    depart_list = [['?cid=1015#doctorList'],
                   ['?cid=332&tabIndex=1#doctorList'],
                   ['?cid=727&tabIndex=1#doctorList'],
                   ['?tabIndex=0&cid=858#doctorList', '?tabIndex=0&cid=49#doctorList'],
                   ['?cid=925&tabIndex=1#doctorList', '?cid=787#doctorList']]
    driver = wd.Chrome(executable_path=driver_path)

    doctor_list = []
    belong_list = []
    academy_list = []
    year_list = []
    
    for idx, city in enumerate(page_list):
        for depart in depart_list[idx]:
            try:
                driver.get(main_url_front + city + main_url_back + depart)
                time.sleep(2)

                doc_list = driver.find_elements_by_css_selector(
                    '#doctorList > div > ul > li'
                )            
                doc_len = len(doc_list)

                for i in range(1, doc_len+1):
                    try:
                        #의료진 페이지 이동
                        driver.find_element_by_css_selector(
                            '#doctorList > div > ul > li:nth-child(%s) > div > div > div > a:nth-child(2)'%(i)
                        ).send_keys(Keys.ENTER)
                        time.sleep(2)

                        #이름 => 교수 제거
                        temp_list = driver.find_element_by_css_selector(
                            '#uiTabPopup01 > div > div.tit-area > h3 > strong'
                        ).text.split(' ')
                        temp_name = temp_list[0]


                        #학회활동
                        academic_list = driver.find_elements_by_css_selector(
                            '#uiTabContent01 > ul:nth-child(4) > li')

                        temp_academic = []
                        temp_year = []
                        check_academic = ['정회원', '회원', '이사', '회장', '위원', '의원', '학회', '조직위', '감사']
                        spec_str = ['▶', '□', '*','1. ']

                        for academic in academic_list:
                            find_year = []
                            contain = False
                            skip = False
                            academic = academic.text.replace("'", '"')

                            #특수 문자열이 들어가있으면 저장하지 않음
                            for spec in spec_str:
                                if spec in academic:
                                    skip = True
                                    break

                            if skip:
                                continue

                            for pos in check_academic:
                                if pos in academic:
                                    contain = True
                                    break

                            if contain:
                                for s in academic:
                                    if s.isdigit():
                                        find_year.append(s)

                                if len(find_year) > 4:
                                    find_year = find_year[:4]
                                elif len(find_year) < 4:
                                    find_year = ''

                                temp_year.append(''.join(find_year))
                                temp_academic.append(academic)

                        #['seoul', 'sanggye', 'ilsan', 'busan', 'haeundae']
                        if idx == 0:
                            temp_belong = '인제대학교서울백병원'
                        elif idx == 1:
                            temp_belong = '인제대학교상계백병원'
                        elif idx == 2:
                            temp_belong = '인제대학교일산백병원'
                        elif idx == 3:
                            temp_belong = '인제대학교부산백병원'
                        else:
                            temp_belong = '인제대학교해운대백병원'

                        #의료진 페이지 나가기
                        driver.find_element_by_css_selector(
                            '#doctorIntroduce > button').click()
                        
                        #데이터 저장
                        doctor_list.append(temp_name)
                        belong_list.append(temp_belong)
                        academy_list.append(temp_academic)
                        year_list.append(temp_year)

                    except Exception as e1:
                        print('의료진 페이지 오류', e1)

            except Exception as e1:
                print( '전체 페이지 오류', e1 )
                
    #DB 저장
    for i in range(len(doctor_list)):    
        try:
            for j in range(len(academy_list[i])):
                if not academy_list[i][j]:
                    academic = None
                else:
                    academic = academy_list[i][j]

                if not year_list[i][j]:
                    year = None
                else:
                    year = year_list[i][j]

                #학회 활동 DB 추가
                sql = """INSERT INTO """+new_table+"""(name_kor, belong, academy, academy_period)
                VALUES(%s, %s, %s, %s)
                """

                cursor.execute(sql, (doctor_list[i], belong_list[i], academic, year))
                conn.commit()

        except Exception as e1:
            print("DB저장 오류 : ", e1)
            conn.close()

            driver.close()
            driver.quit()
            import sys
            sys.exit()

    driver.close()
    driver.quit()


