#!/usr/bin/env python
# coding: utf-8

# In[41]:




#분당서울대학교병원

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
        if row[1] == '분당서울대학교병원':
            name = row[0]
            link = row[5]

            if link[70] == '=':
                start_idx = 71
            else:
                start_idx = 72

            if link[-8] == '&':
                end_idx = -7
            else:
                end_idx = -8

            doctor_num = link[start_idx : end_idx]

            first_url = 'https://www.snubh.org/common/popup/drIntroduce_view.do?sDpCdDtl='
            last_url = 'S_DP_CD=CVC&MENU_ID=001001&DP_CD=EN'
            link = first_url + doctor_num + last_url
            temp_name = ''

            try:
                try:
                    driver.implicitly_wait(5)
                    driver.get(link)
                    temp_name = driver.find_element_by_css_selector(
                        '#wrapper > div > div > div.profile_info > div.info_box > p'
                    ).text
                except:
                    try:
                        last_url = 'S_DP_CD=IMC&MENU_ID=001001&DP_CD=EN'
                        link = first_url + doctor_num + last_url

                        driver.implicitly_wait(5)
                        driver.get(link)
                        temp_name = driver.find_element_by_css_selector(
                            '#wrapper > div > div > div.profile_info > div.info_box > p'
                        ).text
                        pass
                    except:
                        try:
                            last_url = 'S_DP_CD=TS&MENU_ID=001001&DP_CD=EN'
                            link = first_url + doctor_num + last_url

                            driver.implicitly_wait(5)
                            driver.get(link)
                            temp_name = driver.find_element_by_css_selector(
                                '#wrapper > div > div > div.profile_info > div.info_box > p'
                            ).text
                            pass
                        except Exception as e1:
                            print(e1)

                #데이터 저장
                doctor_list.append(name)
                eng_list.append(temp_name)
                

            except Exception as e1:
                print("의료진 페이지 오류 : ", e1)
            
    #DB 저장
    for i in range(len(doctor_list)):    
        try:
            if not eng_list[i] or not eng_list[i][0].encode().isalpha():
                eng_list[i] = None

            sql = """INSERT INTO """+new_table+"""(name_kor, belong, name_eng)
            VALUES(%s, %s, %s)
            """

            cursor.execute(sql, (doctor_list[i], "분당서울대학교병원", eng_list[i]))
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
