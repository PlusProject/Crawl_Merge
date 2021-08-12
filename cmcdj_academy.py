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
        if row[1] == '가톨릭대학교대전성모병원':
            name = row[0]
            link = row[5]

            try:
                driver.implicitly_wait(10)
                driver.get(link)

                #학력/경력/학회활동
                temp_academic = []
                temp_year = []

                data_list = driver.find_elements_by_css_selector(
                    'body > div.section-white > div > div > div > ul > li'
                )

                for data in data_list:
                    data = data.text
                    #학회활동
                    if "정회원" in data or "회원" in data:
                        find_year = []
                        for s in data:
                            if s.isdigit() or s == '~' or s == '-':
                                find_year.append(s)

                        temp_year.append(''.join(find_year))
                        temp_academic.append(data)
                        
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
                    academic = None
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

                cursor.execute(sql, (doctor_list[i], "카톨릭대학교대전성모병원", academic, year))
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



