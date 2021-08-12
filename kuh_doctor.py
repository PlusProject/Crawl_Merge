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

def doctor(conn, cursor, new_table, driver_path):

    main_url = 'https://www.kuh.ac.kr/medical/dept/deptDoctor.do?dept_cd='
    driver = wd.Chrome(executable_path=driver_path)
    page_list = ['000204', '100004', '100035', '300002', '300014']

    # all_name => doctor_list
    doctor_list = []
    major_list = []
    edu_list = []
    career_list = []
    link_list = []
    hospital_code = '143110'

    #for page in page_list:
    for page in page_list:
        try:
            driver.get(main_url + page)
            time.sleep(2)

            docTreatInfo_col = []
            docTreatInfo_col = driver.find_elements_by_class_name("docTreatInfo")
            docTreatInfo_col_len = len(docTreatInfo_col)

            for col in range(docTreatInfo_col_len):
                col_list = driver.find_elements_by_css_selector(
                    "#content > div.treatInfoCont > div:nth-child(%s) > div"%(col+3))
                col_len = len(col_list)

                for i in range(1, col_len+1):
                    try:
                        #의료진 페이지 들어가기
                        driver.find_element_by_css_selector(
                            "#content > div.treatInfoCont > div:nth-child(%s) > div:nth-child(%s) > div.docSchedule > div > a"%(col+3, i)).click()
                        time.sleep(2)

                        temp_name = driver.find_element_by_css_selector(
                            "#content > div.blogDoctor > div.docInfo > div.desc > strong").text
                        #이름 중복 검사
                        if temp_name in doctor_list:
                            driver.back()
                            continue
                        else:
                            pass

                        #진료과
                        temp_major = []
                        temp_major.append(driver.find_element_by_css_selector(
                            "#content > div.blogDoctor > div.docInfo > div.desc > p").text)

                        #학력
                        education_list = driver.find_elements_by_css_selector(
                            "#blogDoc01 > div > div.item.icon01 > ul > li")
                        temp_edu = []
                        for edu in education_list:
                            edu = edu.text
                            edu = edu.replace("|", "", 10)
                            edu = edu.strip(" ")
                            temp_edu.append(edu)

                        #경력
                        career_data = driver.find_elements_by_css_selector(
                            "#blogDoc01 > div > div.item.icon02 > ul > li")
                        temp_career = []
                        for career in career_data:
                            career = career.text
                            career = career.replace("|", "", 10)
                            career = career.strip(" ")
                            temp_career.append(career)

                        temp_link = driver.current_url

                        #의료진 페이지 나가기
                        driver.back()

                        #DB 저장
                        doctor_list.append(temp_name)
                        major_list.append(temp_major)
                        edu_list.append(temp_edu)
                        career_list.append(temp_career)
                        link_list.append(temp_link)

                    except Exception as e1:
                        print( '의료진 페이지 검색 오류', e1 )

        except Exception as e1:
            print( '전체 페이지 검색 오류', e1 )

    #DB 저장
    for i in range(len(doctor_list)):
        try:
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
            VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')
            """%(doctor_list[i], '건국대학교병원', major, education, career, link_list[i], hospital_code)

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
