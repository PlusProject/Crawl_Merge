#양산부산대하교병원 심혈관센터 : http://cc.pnuyh.or.kr/TCF/cb/treat/docList.do?menuIdx=12&id=1
#부산대학교어린이병원 소아심장센터 : http://ptsphc.pnuyh.or.kr/TCF/cb/treat/docList.do?menuIdx=12&id=56

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
    belong_list = []
    scholar_list = []

    for row in select:
        if row[1] == '양산부산대학교병원' or row[1] == '부산대학교어린이병원':
            name = row[0]
            belong = row[1]
            link = row[5]

            try:
                driver.implicitly_wait(10)
                driver.get(link)

                #논문 페이지 들어가기
                driver.implicitly_wait(10)
                driver.find_element_by_css_selector(
                    "#contents_ws > div.profileWrap > div.profile > ul.tabTypeA > li:nth-child(2) > a"
                ).click()

                paper_text = driver.find_element_by_xpath(
                    "//*[@id='contents_ws']/div[4]/div[2]/p"
                ).text.strip('\n')
                paper_list = [data for data in paper_text.split("\n")]
                temp_paper = []

                #논문 따옴표(') & 저널 예외 처리
                for paper in paper_list:
                    p_name = paper

                    if p_name == "- 그 외 다수" or p_name =='' or p_name == '논문)' or p_name == '저서)' or '회원' in p_name:
                        continue
                    else:
                        for i in range(3):
                            if p_name[i].isdigit() or p_name[i] == '.':
                                p_name = p_name[:i] + ' ' + p_name[i+1:]

                        #따옴표 처리
                        p_name = p_name.replace("'", "''", 10)
                        p_name = p_name.replace("[", " ", 10)
                        p_name = p_name.replace("]", " ", 10)
                        p_name = p_name.strip(" ")
                        temp_paper.append(p_name)

                #데이터 저장
                doctor_list.append(name)
                belong_list.append(belong)
                scholar_list.append(temp_paper)


            except Exception as e1:
                print( '의료진 페이지 검색 오류', e1 )

    #DB 저장
    for i in range(len(doctor_list)):
        try:
            #논문 DB 추가
            for j in range(len(scholar_list[i])):

                sql = """INSERT INTO """+new_table+"""(name_kor, belong, pname)
                VALUES('%s', '%s', '%s')
                """%(doctor_list[i], belong_list[i], scholar_list[i][j])

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
