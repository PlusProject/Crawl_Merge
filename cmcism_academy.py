#카톨릭대학교 인천성모병원
#심장혈관내과 : https://www.cmcism.or.kr/treatment/treatment_team?deptSeq=36
#흉부외과 : https://www.cmcism.or.kr/treatment/treatment_team?deptSeq=50

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pymysql


def academy(conn, cursor, new_table, doctor_table, driver_path):
    
    main_url = 'https://www.cmcism.or.kr/treatment/treatment_team?deptSeq='
    depart_list = ['36', '50']
    driver = wd.Chrome(executable_path=driver_path)
    
    doctor_list = []
    academy_list = []
    year_list = []

    for depart in depart_list:
        try:
            driver.implicitly_wait(10)
            driver.get(main_url + depart)

            click_page = '#right > div.sub_wrap > div.Team_write > div > div'
            doc_list = driver.find_elements_by_css_selector(click_page)
            doc_num = len(doc_list)

            for doctor in doc_list:
                try:
                    id_name = doctor.find_element_by_css_selector('a').get_attribute("id")
                    id_name = id_name.split("_")
                    id_num = id_name[2]

                    doctor.find_element_by_css_selector('a').send_keys(Keys.ENTER)
                    time.sleep(2)

                    #이름
                    temp_name = driver.find_element_by_css_selector(
                        '#tab%s_1 > div > div.text_box > div > ul > li.li_h > span'%(id_num)
                    ).text
                    temp_name = temp_name[:-2]

                    #학회활동 페이지 클릭
                    driver.find_element_by_css_selector(
                        '#layer_pop_%s > div > ul > li:nth-child(2)'%(id_num)
                    ).click()
                    time.sleep(2)

                    #학회활동
                    temp_academic = []
                    temp_year = []

                    academic_list = driver.find_elements_by_css_selector(
                        '#tab%s_2 > dl:nth-child(3) > dd'%(id_num)
                    )

                    for academic in academic_list:
                        academic = academic.text
                        find_year = []

                        for s in academic:
                            if s.isdigit() or s == '.' or s == '~' or s == '-':
                                find_year.append(s)

                        temp_year.append(''.join(find_year))
                        temp_academic.append(academic)

                    #데이터 저장
                    doctor_list.append(temp_name)
                    academy_list.append(temp_academic)
                    year_list.append(temp_year)

                    #팝업창 닫기 => 의료진 페이지 닫기
                    driver.find_element_by_css_selector('#btn_close_'+id_num).send_keys(Keys.ENTER)

                except Exception as e1:
                    print("의료진 페이지 오류 : ", e1)

        except Exception as e1:
            print("전체 페이지 오류 : ", e1)
            
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
                    if len(year_list[i][j]) > 4:
                        year = year_list[i][j][:4]
                    else:
                        year = year_list[i][j]

                #학회 활동 DB 추가
                sql = """INSERT INTO """+new_table+"""(name_kor, belong, academy, academy_period)
                VALUES(%s, %s, %s, %s)
                """

                cursor.execute(sql, (doctor_list[i], "카톨릭대학교인천성모병원", academic, year))
                conn.commit()

        except Exception as e1:
            print("DB 저장 오류 : ", e1)
            conn.close()

            driver.close()
            driver.quit()
            import sys
            sys.exit()

    driver.close()
    driver.quit()
