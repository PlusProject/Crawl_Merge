#양산부산대하교병원 심혈관센터 : http://cc.pnuyh.or.kr/TCF/cb/treat/docList.do?menuIdx=12&id=1
#부산대학교어린이병원 소아심장센터 : http://ptsphc.pnuyh.or.kr/TCF/cb/treat/docList.do?menuIdx=12&id=56

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
    belong_list = []
    academy_list = []
    year_list = []

    for row in select:
        if row[1] == '양산부산대학교병원' or row[1] == '부산대학교어린이병원':
            name = row[0]
            belong = row[1]
            link = row[5]

            try:
                driver.implicitly_wait(10)
                driver.get(link)

                #학회 활동
                academic_text = driver.find_element_by_xpath(
                    "//*[@id='contents_ws']/div[4]/div[2]/ul[4]/li"
                ).text.strip('\n')
                academic_list = [data for data in academic_text.split("\n")]

                temp_academic = []
                temp_year = []

                for academic in academic_list:
                    find_year = []

                    if academic == '':
                        continue

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
                belong_list.append(belong)
                academy_list.append(temp_academic)
                year_list.append(temp_year)


            except Exception as e1:
                print( '의료진 페이지 검색 오류', e1 )

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

                cursor.execute(sql, (doctor_list[i], belong_list[i], academic, year))
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





