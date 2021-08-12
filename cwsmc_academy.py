#삼성창원병원
#순환기내과 : http://smc.skku.edu/smc_main/care/treatDoctor.smc?meddept=IC
#흉부외과 : http://smc.skku.edu/smc_main/care/treatDoctor.smc?meddept=TS

from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pymysql

def academy(conn, cursor, new_table, doctor_table, driver_path):

    main_url = "http://smc.skku.edu/smc_main/care/treatDoctor.smc?meddept="
    depart_list = ['IC', 'TS']
    driver = wd.Chrome(executable_path=driver_path)
    
    doctor_list = []
    academy_list = []
    year_list = []

    for depart in depart_list:
        try:
            driver.get(main_url + depart)
            time.sleep(2)

            doc_list = driver.find_elements_by_css_selector(
                '#contents > form > div > div > ul > li'
            )
            doc_len = len(doc_list)
            #contents > form > div > div > ul > li:nth-child(1) > div.txt_box > a

            for i in range(1, doc_len+1):
                try:
                    driver.find_element_by_css_selector(
                        '#contents > form > div > div > ul > li:nth-child(%s) > div.txt_box > a'%(i)
                    ).send_keys(Keys.ENTER)
                    time.sleep(2)

                    #이름
                    temp_list = driver.find_element_by_css_selector(
                            '#contents > form > div > div > div.basic > div.txt_box02 > dl.first > dd:nth-child(2)'
                    ).text.split(' ')
                    temp_name = temp_list[0]

                    #학력, 경력, 학회 및 기타활동
                    data_list = driver.find_element_by_xpath(
                        '//*[@id="contents"]/form/div/div/div[2]/div[2]/dl[3]/dd'
                    ).text.split("\n")

                    temp_academic = []
                    temp_year = []

                    academic = False    

                    for data in data_list:
                        if data == "▶ 학력":
                            edu = True
                            career = False
                            academic = False
                            continue
                        elif data == "▶ 경력":
                            edu = False
                            career = True
                            academic = False
                            continue
                        elif data == "▶ 학회 및 기타활동":
                            edu = False
                            career = False
                            academic = True
                            continue
                        elif "현)" in data:
                            edu = False
                            career = True
                            academic = False
                        elif data == "":
                            continue

                        data = data.replace("-", "")
                        data = data.strip(" ")

                        if academic:
                            find_year = []

                            for s in data:
                                if s.isdigit() or s == '.' or s == '~' or s == '-':
                                    find_year.append(s)

                            temp_year.append(''.join(find_year))
                            temp_academic.append(data)

                    driver.back()

                    #데이터 저장
                    doctor_list.append(temp_name)
                    academy_list.append(temp_academic)
                    year_list.append(temp_year)

                except Exception as e1:
                    print("의료진 페이지 오류 : ", e1)

        except Exception as e1:
            print("전체 페이지 오류 : ", e1)
            
            
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
                    if len(year_list[i][j]) > 7:
                        year = year_list[i][j][:7]
                    else:
                        year = year_list[i][j]

                #학회 활동 DB 추가
                sql = """INSERT INTO """+new_table+"""(name_kor, belong, academy, academy_period)
                VALUES(%s, %s, %s, %s)
                """

                cursor.execute(sql, (doctor_list[i], "삼성창원병원", academic, year))
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


