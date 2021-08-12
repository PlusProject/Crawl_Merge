#!/usr/bin/env python
# coding: utf-8

# In[1]:


#강북삼성병원
#순환기내과 : https://www.kbsmc.co.kr/paramedic/paramedic05_1.jsp?cmnm=순환기내과&chk_cmcd=MC
#흉부외과 : https://www.kbsmc.co.kr/paramedic/paramedic05_1.jsp?cmnm=흉부외과&chk_cmcd=CS


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
    sql = """SELECT * FROM """ + doctor_table
    cursor.execute(sql)
    select = list(cursor.fetchall())
    conn.commit()

    doctor_list = []
    academic_list = []
    year_list = []

    for row in select:
        if row[1] == '강북삼성병원':
            name = row[0]
            link = row[5]

            try:
                driver.implicitly_wait(10)
                driver.get(link)

                #학회
                driver.find_element_by_css_selector(
                    '#sub_Container > div.contents > div > div > div.doc_li_T > a:nth-child(5)'
                ).send_keys(Keys.ENTER)
                time.sleep(2)

                data_list = driver.find_element_by_css_selector(
                    '#t4 > td > dl > dd > ul > li'
                ).text.split("\n")
                #print(academic_list)

                temp_academic = []
                temp_year = []
                check_academic = [
                    '회원', '위원', '간사', '이사', '의원', '회장', '소장', '협회', '학회', 'Assocication', 'Network'
                    ]

                for academic in data_list:
                    find_year = []
                    skip = True

                    if academic == "" or '[' in academic:
                        continue

                    for check in check_academic:
                        if check in academic:
                            skip = False
                            break

                    if not skip:
                        academic = academic.strip(' ')

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
                academic_list.append(temp_academic)
                year_list.append(temp_year)


            except Exception as e1:
                print("의료진 페이지 오류 : ", e1)

    for i in range(len(doctor_list)):
        try:
            for j in range(len(academic_list[i])):
                if not academic_list[i][j]:
                    academic = None
                else:
                    academic = academic_list[i][j]

                if not year_list[i][j]:
                    year = None
                else:
                    year = year_list[i][j]

                #학회 활동 DB 추가
                sql = """INSERT INTO """+new_table+"""(name_kor, belong, academy, academy_period)
                VALUES(%s, %s, %s, %s)
                """

                cursor.execute(sql, (doctor_list[i], '강북삼성병원', academic, year))
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
