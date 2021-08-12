#삼성창원병원
#순환기내과 : http://smc.skku.edu/smc_main/care/treatDoctor.smc?meddept=IC
#흉부외과 : http://smc.skku.edu/smc_main/care/treatDoctor.smc?meddept=TS

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pymysql

def engName(conn, cursor, new_table, doctor_table, driver_path):

    main_url = "http://smc.skku.edu/smc_main/care/treatDoctor.smc?meddept="
    depart_list = ['IC', 'TS']
    driver = wd.Chrome(executable_path=driver_path)
    
    doctor_list = []
    eng_list = []

    for depart in depart_list:
        try:
            driver.get(main_url + depart)
            time.sleep(2)

            doc_list = driver.find_elements_by_css_selector(
                '#contents > form > div > div > ul > li'
            )
            doc_len = len(doc_list)
            #contents > form > div > div > ul > li:nth-child(1) > div.txt_box > a

            for i in range(1, doc_len+1):
                try:
                    driver.find_element_by_css_selector(
                        '#contents > form > div > div > ul > li:nth-child(%s) > div.txt_box > a'%(i)
                    ).send_keys(Keys.ENTER)
                    time.sleep(2)

                    #이름
                    temp_list = driver.find_element_by_css_selector(
                            '#contents > form > div > div > div.basic > div.txt_box02 > dl.first > dd:nth-child(2)'
                    ).text.split(' ')
                    temp_name_kor = temp_list[0]

                    #영문 정보
                    driver.find_element_by_css_selector(
                        '#contents > form > div > div > div.tab_box > ul > li:nth-child(2) > a'
                    ).send_keys(Keys.ENTER)

                    temp_name_eng = driver.find_element_by_css_selector(
                        '#contents > form > div > div > div.basic > div.txt_box02 > dl.first > dd'
                    ).text

                    temp_name_eng = temp_name_eng.replace('-', ' ')
                    temp_name_eng = temp_name_eng.split(' ')
                    temp_name_eng = ' '.join(temp_name_eng[:3])

                    driver.back()
                    driver.back()

                    #데이터 저장
                    doctor_list.append(temp_name_kor)
                    eng_list.append(temp_name_eng)

                except Exception as e1:
                    print("의료진 페이지 오류 : ", e1)

        except Exception as e1:
            print("전체 페이지 오류 : ", e1)

            
    #DB 저장
    for i in range(len(doctor_list)): 
        try:
            if not eng_list[i]:
                eng_list[i] = None

            #의료진 DB 추가
            sql = """INSERT INTO """+new_table+"""(name_kor, belong, name_eng)
            VALUES(%s, %s, %s)
            """

            cursor.execute(sql, (doctor_list[i], "삼성창원병원", eng_list[i]))
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



