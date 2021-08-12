#!/usr/bin/env python
# coding: utf-8

# In[4]:


#분당서울대학교병원

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pymysql

def scholar(conn, cursor, new_table, doctor_table, driver_path):

    driver = wd.Chrome(executable_path=driver_path)

    # table 불러오기
    sql = """SELECT * FROM """+doctor_table
    cursor.execute(sql)
    select = list(cursor.fetchall())
    conn.commit()

    doctor_list = []
    scholar_list = []

    for row in select:
        if row[1] == '분당서울대학교병원':
            name = row[0]
            link = row[5]

            try:
                driver.implicitly_wait(10)
                driver.get(link)

                #연구업적 탭
                driver.implicitly_wait(10)
                driver.find_element_by_css_selector('#tab_4 > a').send_keys(Keys.ENTER)

                #논문
                temp_paper = []
                check_dup_paper = []
                #논문제목 기재 방식이 다른 의료진
                if name == "이재항":
                    paper_list = driver.find_elements_by_css_selector(
                    '#cont_wrap4 > div:nth-child(2) > ul > li')

                    for paper in paper_list:
                        p_name = paper.text
                        p_name = p_name.strip(" ")
                        p_name = p_name.replace("'", "''", 10)

                        #중복 검사
                        if p_name.lower() in check_dup_paper:
                            continue

                        check_dup_paper.append(p_name.lower())
                        temp_paper.append(p_name)

                else:
                    try:
                        paper_list = driver.find_elements_by_css_selector(
                            '#cont_wrap4 > div:nth-child(1) > ul > li')
                        paper_len = len(paper_list)

                        for i in range(1, paper_len+1):
                            p_name = driver.find_element_by_css_selector(
                                '#cont_wrap4 > div:nth-child(1) > ul > li:nth-child(%s) > p.title'%(i)
                            ).text
                            p_name = p_name.strip(" ")
                            p_name = p_name.replace("'", "''", 10)

                            #중복 검사
                            if p_name.lower() in check_dup_paper:
                                continue

                            check_dup_paper.append(p_name.lower())
                            temp_paper.append(p_name)

                    except:
                        paper_list = driver.find_elements_by_css_selector(
                            '#cont_wrap4 > div:nth-child(1) > ul > li')
                        paper_len = len(paper_list)

                        for paper in paper_list:
                            p_name = paper.text
                            p_name = p_name.replace("\n", ", ", 10)
                            p_name = p_name.replace("'", "''", 10)

                            #중복 검사
                            if p_name.lower() in check_dup_paper:
                                continue

                            check_dup_paper.append(p_name.lower())
                            temp_paper.append(p_name)

                #데이터 저장
                doctor_list.append(name)
                scholar_list.append(temp_paper)

            except Exception as e1:
                print("의료진 페이지 오류 : ", e1)

    for i in range(len(doctor_list)):    
        try:
            #논문 DB 추가
            for j in range(len(scholar_list[i])):
                sql = """INSERT INTO """+new_table+"""(name_kor, belong, pname)
                VALUES('%s', '%s', '%s')
                """%(doctor_list[i], "분당서울대학교병원", scholar_list[i][j])

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
