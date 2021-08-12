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

def doctor(conn, cursor, new_table, driver_path):

    main_url= 'https://www.kbsmc.co.kr/paramedic/paramedic05_1.jsp?cmnm='
    depart_list = ['순환기내과&chk_cmcd=MC', '흉부외과&chk_cmcd=CS']
    driver = wd.Chrome(executable_path=driver_path)

    doctor_list = []
    major_list = []
    edu_list = []
    career_list = []
    link_list = []
    hospital_code = "110110"
    belong = "강북삼성병원"

    for depart in depart_list:
        try:
            driver.implicitly_wait(10)
            driver.get(main_url + depart)

            doc_list = driver.find_elements_by_css_selector(
                '#resultArea > div'
            )
            doc_len = len(doc_list)

            for i in range(1, doc_len+1):
                try:
                    driver.implicitly_wait(10)
                    driver.find_element_by_css_selector(
                        '#resultArea > div:nth-child(%s) > div.doc_li_L > a:nth-child(3)'%(i)
                    ).click()

                    time.sleep(2)

                    #의료진 개인 페이지
                    temp_link = driver.current_url

                    #이름
                    temp_name = driver.find_element_by_css_selector(
                        '#sub_Container > div.contents > div > div > div.doc_li_T > div > p.name'
                    ).text

                    #진료과
                    temp_major = []
                    temp_major.append(driver.find_element_by_css_selector(
                        '#t1 > td > dl > dd > ul > li'
                    ).text)

                    #학력 & 경력
                    data_list = driver.find_element_by_xpath(
                        '//*[@id="t3"]/td/dl/dd/ul/li'
                    ).text.split("\n")

                    temp_edu = []
                    temp_career = []

                    for data in data_list:
                        if data == "" or data in ["[학력]", "[경력]", "[학력/경력]", "[수련]"] or '논문제목' in data:
                            continue
                        elif data.find("박사") != -1 or data.find("석사") != -1 or data.find("학사") != -1 or data.find("졸업") != -1:
                            data = data.strip(' ')
                            temp_edu.append(data)
                        else:
                            data = data.strip(' ')
                            temp_career.append(data)

                    driver.back()

                    #데이터 저장
                    doctor_list.append(temp_name)
                    major_list.append(temp_major)
                    edu_list.append(temp_edu)
                    career_list.append(temp_career)
                    link_list.append(temp_link)

                except Exception as e1:
                    print("의료진 페이지 오류 : ", e1)

        except Exception as e1:
            print("전체 페이지 오류 : ", e1)

    #DB 저장
    for i in range(len(doctor_list)):
        try:
            if not major_list[i][0]:
                major = None
            else:
                major = major_list[i][0]

            if not edu_list[i]:
                education = None
            else:
                education = ', '.join(edu_list[i])

            if not career_list[i]:
                career = None
            else:
                career = ', '.join(career_list[i])

            #의료진 DB 추가
            sql = """INSERT INTO """+new_table+"""(name_kor, belong, major, education, career, link, hospital_code)
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (doctor_list[i], '강북삼성병원', major, education, career, link_list[i], hospital_code))
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
