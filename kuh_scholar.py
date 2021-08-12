#건군대학교병원
#심장혈관내과 : dept_cd=000204
#심장혈관센터 : dept_cd=100004
#대동맥혈관센터 : dept_cd=100035
#관상동맥질환클리닉 : dept_cd=300002
#심부전클리닉 ; dept_cd=300014

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    #for page in page_list:
    for row in select:
        if row[1] == '건국대학교병원':
            temp_name = row[0]
            link = row[5]

            try:
                driver.get(link)
                time.sleep(2)

                #논문 페이지 들어가기
                driver.find_element_by_css_selector(
                    "#content > div.blogDoctor > div.docProfile > ul > li:nth-child(2) > a").click()
                time.sleep(2)

                paper_list = driver.find_elements_by_css_selector(
                    "#blogDoc02 > div > div > ul > li")
                temp_paper = []

                #작은 따옴표(')예외처리
                for paper in paper_list:
                    p_name = paper.find_element_by_css_selector("strong").text
                    p_name = p_name.replace("'", "''", 10)

                    temp_paper.append(p_name)

                #데이터 저장
                doctor_list.append(temp_name)
                scholar_list.append(temp_paper)


            except Exception as e1:
                print( '의료진 페이지 검색 오류', e1 )

    #DB 저장
    for i in range(len(doctor_list)):     
        try:
            for j in range(len(scholar_list[i])):
                sql = """INSERT INTO """+new_table+"""(name_kor, belong, pname)
                VALUES('%s', '%s', '%s')
                """%(doctor_list[i], '건국대학교병원', scholar_list[i][j])

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
