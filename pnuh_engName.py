from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
import pymysql

def engName(conn, cursor, new_table, doctor_table, driver_path):

    driver = wd.Chrome(executable_path=driver_path)

    # table 불러오기
    sql = """SELECT * FROM """+doctor_table
    cursor.execute(sql)
    select = list(cursor.fetchall())
    conn.commit()

    doctor_list = []
    belong_list = []
    eng_list = []

    for row in select:
        if row[1] == '양산부산대학교병원' or row[1] == '부산대학교어린이병원':
            name = row[0]
            belong = row[1]

            link = row[5]
            doctor_num = str(link[-7:])

            if belong == '양산부산대학교병원':
                link = 'https://www.pnuyh.or.kr/english/treat/doctorInfo.do?rbsIdx=58&type=1&code=CC&dno=' + doctor_num
            else:
                link = 'https://www.pnuyh.or.kr/english/treat/doctorInfo.do?rbsIdx=59&type=1&code=PTSPHC&dno=' + doctor_num

            try:
                #driver.implicitly_wait(5)
                try:
                    driver.set_page_load_timeout(5)
                    driver.get(link)
                except TimeoutException as ex:
                    isrunning = 0
                    print("Exception has been thrown. " + str(ex))
                    pass

                temp_name = driver.find_element_by_css_selector(
                    '#contents_area > div.psnlTitle > h4').text
                
                #DB 저장
                doctor_list.append(name)
                belong_list.append(belong)
                eng_list.append(temp_name)

            except Exception as e1:
                print( '의료진 페이지 검색 오류', e1 )
            
    for i in range(len(doctor_list)):
        try:
            if not eng_list[i]:
                eng_list[i] = None
        
            sql = """INSERT INTO """+new_table+"""(name_kor, belong, name_eng)
            VALUES(%s, %s, %s)
            """

            cursor.execute(sql, (doctor_list[i], belong_list[i], eng_list[i]))
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




