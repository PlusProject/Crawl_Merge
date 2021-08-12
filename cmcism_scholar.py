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


def scholar(conn, cursor, new_table, doctor_table, driver_path):

    main_url = 'https://www.cmcism.or.kr/treatment/treatment_team?deptSeq='
    depart_list = ['36', '50']
    driver = wd.Chrome(executable_path=driver_path)
    
    doctor_list = []
    scholar_list = []

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
                    #print(temp_name)

                    #논문
                    temp_paper = []
                    try:
                        #논문 페이지 클릭
                        driver.find_element_by_css_selector(
                            '#layer_pop_%s > div > ul > li:nth-child(3)'%(id_num)
                        ).click()
                    except:
                        pass
                    else:
                        time.sleep(2)

                        paper_list = driver.find_elements_by_css_selector(
                            '#tab%s_3 > dl > dd'%(id_num)
                        )

                        for paper in paper_list:
                            p_name = paper.text
                            p_name = p_name.replace("'", "''", 10)
                            temp_paper.append(p_name)
                    #print(temp_paper)

                    #데이터 저장
                    doctor_list.append(temp_name)
                    scholar_list.append(temp_paper)

                    #팝업창 닫기 => 의료진 페이지 닫기
                    driver.find_element_by_css_selector('#btn_close_'+id_num).send_keys(Keys.ENTER)

                except Exception as e1:
                    print("의료진 페이지 오류 : ", e1)

        except Exception as e1:
            print("전체 페이지 오류 : ", e1)

            
    #DB 저장
    for i in range(len(doctor_list)):
        try:
            #논문 DB 추가
            for j in range(len(scholar_list[i])):
                sql = """INSERT INTO """+new_table+"""(name_kor, belong, pname)
                VALUES('%s', '%s', '%s')
                """%(doctor_list[i], "카톨릭대학교인천성모병원", scholar_list[i][j])

                cursor.execute(sql)
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
