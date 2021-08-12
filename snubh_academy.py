#!/usr/bin/env python
# coding: utf-8

# In[1]:


#분당서울대학교병원

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pymysql


def academy(conn, cursor, new_table, doctor_table, driver_path):

    driver = wd.Chrome(executable_path=driver_path)

    # table 불러오기
    sql = """SELECT * FROM """+doctor_table
    cursor.execute(sql)
    select = list(cursor.fetchall())
    conn.commit()

    doctor_list = []
    academy_list = []
    year_list = []

    for row in select:
        if row[1] == '분당서울대학교병원':
            name = row[0]
            link = row[5]

            try:
                driver.implicitly_wait(10)
                driver.get(link)

                #학력/경력/활동 탭
                driver.implicitly_wait(10)
                driver.find_element_by_css_selector('#tab_3 > a').send_keys(Keys.ENTER)

                cont_num = driver.find_elements_by_css_selector(
                    '#cont_wrap3 > div')
                cont_len = len(cont_num)

                #활동
                temp_academic = []
                temp_year = []

                academic_list = driver.find_elements_by_css_selector(
                    '#cont_wrap3 > div:nth-child(%s) > ul > li'%(cont_len))

                for academic in academic_list:
                    academic = academic.text
                    find_year = []

                    if academic == '수상':
                        break

                    for s in academic:
                        if s.isdigit():
                            find_year.append(s)

                    if len(find_year) > 4:
                        find_year = find_year[:4]
                    elif len(find_year) < 4:
                        find_year = ''

                    temp_year.append(''.join(find_year))
                    temp_academic.append(academic)

                #데이터 저장
                doctor_list.append(name)
                academy_list.append(temp_academic)
                year_list.append(temp_year)

            except Exception as e1:
                print("의료진 페이지 오류 : ", e1)
                

    #DB 저장
    for i in range(len(doctor_list)):
        try:
            for j in range(len(academy_list[i])):
                if not academy_list[i][j]:
                    continue
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

                cursor.execute(sql, (doctor_list[i], "분당서울대학교병원", academic, year))
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

