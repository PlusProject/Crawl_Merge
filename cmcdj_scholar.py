#카톨릭대학교 대전성모병원
#심장내과 : 
#https://www.cmcdj.or.kr/servlet/MainSvl?_tc=F001001001002&cd2=001&cd3=001&cd4=001&cd5=002&deptidx=111
#흉부외과 : 
#https://www.cmcdj.or.kr/servlet/MainSvl?_tc=F001001001002&cd2=001&cd3=001&cd4=001&cd5=002&deptidx=156

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
        if row[1] == '가톨릭대학교대전성모병원':
            name = row[0]
            link = row[5]

            try:
                driver.implicitly_wait(10)
                driver.get(link)

                #논문
                temp_paper = []

                child_list = driver.find_elements_by_css_selector(
                    'body > div.section-gray > div > div > div > *'
                )

                child_len = len(child_list)

                for j in range(2, child_len+1):
                    find = False
                    try:
                        cont_name = driver.find_element_by_css_selector(
                            'body > div.section-gray > div > div > div > p:nth-child(%s) > span > *'%(j)
                        ).text

                    except:
                        try:
                            cont_name = driver.find_element_by_css_selector(
                                'body > div.section-gray > div > div > div > div:nth-child(%s) > b'%(j)
                            ).text
                        except:
                            continue
                        else:
                            if "연구" in cont_name:
                                find = True
                                paper_list = driver.find_elements_by_css_selector(
                                    'body > div.section-gray > div > div > div > div:nth-child(%s) > ul > li'%(j+1)
                                )

                    else:
                        if "논문" in cont_name:
                            find = True
                            paper_list = driver.find_elements_by_css_selector(
                                'body > div.section-gray > div > div > div > ul:nth-child(%s) > li'%(j+1)
                            )

                    if find:
                        for paper in paper_list:
                            p_name = paper.text
                            if p_name == "":
                                continue

                            p_name = p_name.strip("\n")
                            p_name = p_name.replace("'", "''", 10)
                            temp_paper.append(p_name)
                        break

                #데이터 저장
                doctor_list.append(name)
                scholar_list.append(temp_paper)

            except Exception as e1:
                print("의료진 페이지 오류 : ", e1)
            
    #DB 저장
    for i in range(len(doctor_list)):
        try:
            for j in range(len(scholar_list[i])):
                sql = """INSERT INTO """+new_table+"""(name_kor, belong, pname)
                VALUES('%s', '%s', '%s')
                """%(doctor_list[i], "카톨릭대학교대전성모병원", scholar_list[i][j])

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
