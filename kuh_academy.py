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
    academic_list = []
    year_list = []

    for row in select:
        if row[1] == '건국대학교병원':
            temp_name = row[0]
            link = row[5]
            try:
                driver.get(link)
                time.sleep(2)

                #학회 활동
                data_list = driver.find_elements_by_css_selector(
                    "#blogDoc01 > div > div.item.icon03 > ul > li")

                temp_academic = []
                temp_year = []

                for academic in data_list:
                    find_year = []
                    academic = academic.text
                    #print(academic)

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
                doctor_list.append(temp_name)
                academic_list.append(temp_academic)
                year_list.append(temp_year)


            except Exception as e1:
                print( '의료진 페이지 검색 오류', e1 )

    #DB 저장
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

                cursor.execute(sql, (doctor_list[i], '건국대학교병원', academic, year))
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


