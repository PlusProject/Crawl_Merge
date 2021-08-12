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
        if row[1] == '강북삼성병원':
            temp_name = row[0]
            link=row[5]

            try:
                driver.get(link)
                time.sleep(2)

                #의료진 개인 페이지
                temp_link = driver.current_url

                #논문
                driver.find_element_by_css_selector(
                    '#sub_Container > div.contents > div > div > div.doc_li_T > a:nth-child(6)'
                ).click()
                time.sleep(2)

                paper_list = driver.find_element_by_xpath(
                    '//*[@id="t5"]/td/dl/dd/ul/li'
                ).text.split("\n")

                temp_paper = []

                for paper in paper_list:
                    p_name = paper
                    p_len = len(p_name)

                    if temp_name == "성기철":
                        pass

                    elif p_name == "" or p_len <= 9:
                        continue

                    #앞 번호 제거 => pubmed 검색 원활
                    if p_len > 3:
                        #2014 논문이름 같은 형식은 넘기기위해
                        if not p_name[3].isdigit():
                            for i in range(3):
                                if p_name[i].isdigit() or p_name[i] == '.' or p_name[i] == '-':
                                    p_name = p_name[:i] + ' ' + p_name[i+1:]

                    p_name = p_name.strip(" ")
                    p_name = p_name.replace("'", "''", 10)
                    p_name = p_name.replace("\xad", "-", 10)
                    p_name = p_name.replace("[", " ", 10)
                    p_name = p_name.replace("]", " ", 10)

                    temp_paper.append(p_name)

                #데이터 저장
                doctor_list.append(temp_name)
                scholar_list.append(temp_paper)

            except Exception as e1:
                print("의료진 페이지 오류 : ", e1)

            #논문 DB 추가
    for i in range(len(doctor_list)):
        try:
            if doctor_list[i] == "김범수":
                for j in range(len(scholar_list[i])):
                    if j%3 == 0:
                        if len(scholar_list[i][j]) <= 14:
                            continue

                        sql = """INSERT INTO """+new_table+"""(name_kor, belong, pname)
                        VALUES('%s', '%s', '%s')
                        """%(doctor_list[i], '강북삼성병원', scholar_list[i][j])

                        cursor.execute(sql)
                        conn.commit()

            elif doctor_list[i] == "성기철":
                for j in range(1, len(scholar_list[i])):
                    if scholar_list[i][j-1] == '':
                        if scholar_list[i][j] == '' or len(scholar_list[i][j]) <= 9:
                            continue

                        sql = """INSERT INTO """+new_table+"""(name_kor, belong, pname)
                        VALUES('%s', '%s', '%s')
                        """%(doctor_list[i], '강북삼성병원', scholar_list[i][j])

                        cursor.execute(sql)
                        conn.commit()

            else:
                for j in range(len(scholar_list[i])):
                    sql = """INSERT INTO """+new_table+"""(name_kor, belong, pname)
                    VALUES('%s', '%s', '%s')
                    """%(doctor_list[i], '강북삼성병원', scholar_list[i][j])

                    cursor.execute(sql)
                    conn.commit()

        except Exception as e1:
            print("DB 저장 오류 : ", e1)
            #DB종류
            conn.close()

            driver.close()
            driver.quit()
            import sys
            sys.exit()


    driver.close()
    driver.quit()




