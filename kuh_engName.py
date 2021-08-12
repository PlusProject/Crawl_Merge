from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
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
    eng_list = []

    for row in select:
        if row[1] == '건국대학교병원':
            name = row[0]
            link = row[5]
            link = link[:22] + 'english/' + link[22:]
            try:
                driver.get(link)
                time.sleep(2)

                temp_name = driver.find_element_by_css_selector(
                '#wrap > div.containner > main > div > div.center-img-content > div > div.name'
                ).text

                #데이터 저장
                doctor_list.append(name)
                eng_list.append(temp_name)

            except Exception as e1:
                print( '의료진 페이지 검색 오류', e1 )
            
    #DB 저장
    for i in range(len(doctor_list)):    
        try:
            if not eng_list[i]:
                eng_list[i] = None

            #학회 활동 DB 추가
            sql = """INSERT INTO """+new_table+"""(name_kor, belong, name_eng)
            VALUES('%s', '%s', '%s')
            """%(doctor_list[i], '건국대학교병원', eng_list[i])

            cursor.execute(sql)
            conn.commit()

        except Exception as e1:
            print("DB저장 오류 : ", e1)
            #DB종류
            conn.close()

            driver.close()
            driver.quit()
            import sys
            sys.exit()

    driver.close()
    driver.quit()
