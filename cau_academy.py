### import ###
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql

def academy(connect, cursor, table_name, driver_path):
    ### 크롬드라이버 생성 ###
    driver=webdriver.Chrome(executable_path=driver_path)


    #department = ['순환기내과', '심장내과', '심장외과', '흉부외과', '심장혈관외과', '소아심장과']

    ### 크롤링 코드 시작 ###
    url="https://ch.cauhs.or.kr/medical/medical.asp?cat_no=02010000"
    driver.get(url)
    departmentLink=[]
    doctor_click=[]
    doctorLink=[]
    data=[]
    ###한번에 커밋하기 위한 작업###
    name_kor=[]
    belong=[]
    aname=[]
    b=[]
    k=0

    #d1=driver.find_element_by_css_selector("#ganada > ul > li:nth-child(36) > a").click()
    data.append(driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div[3]/div/div[1]/ul/li[14]/a'))
    data.append(driver.find_element_by_xpath('/html/body/div/div[4]/div[2]/div[3]/div/div[1]/ul/li[36]/a'))


    
    for a in data:
        departmentLink.append(a.get_attribute("href"))
    #print(departmentLink)
    for i in departmentLink:
        driver.get(i)
        time.sleep(1)
        buttons=driver.find_elements_by_xpath('//*[@id="content"]/div/div/div[3]/ul/li/div[1]/a')
        #print(len(buttons))
        for m in buttons:
            
                m.click()
                driver.switch_to_window(driver.window_handles[1])
                time.sleep(2)
            
                ### name_kor 수집 ###
                name_kor.append(driver.find_element_by_css_selector('body > div > div.doc_content_wrap > div > div.doctor_txt > div.tit_area.fix > p.doctor_name'))
                name_kor[k]=name_kor[k].text
                #print(name_kor[k])
                # k=k+1
                ### belong 수집: notion_대학병원이름에서 병원 명칭(홈페이지)이름으로 저장 ###
                belong="중앙대학교병원"
                ###aname수집###
                pclick=driver.find_element_by_css_selector('#tab2 > a').click()
                time.sleep(2)
                #print(driver.window_handles)
                driver.switch_to_window(driver.window_handles[1])

                #print(driver.current_url)
                
                
                
                if(len(driver.find_elements_by_xpath("//*[contains(text(),'학회활동')]"))!=0):
                    aname.append(driver.find_element_by_xpath("//*[contains(text(),'학회활동')]//following::ul[1]"))
                    aname[k]=aname[k].text
                    aname[k]=aname[k].split('\n')
                    # print(aname[k])
                    #print(k)
                    
                else:#학회가 없는 경우 0으로 채워넘(기존의 학회활동이라는 글자가 존재하는 의사에서 학회가 없을때 0으로 표시되어있음)
                    
                    #print(k)
                    a=['0']
                    aname.append(a)
                    # print(aname[k])
                b.append([])
                for i in range(len(aname[k])):
                    #print(aname[k][i])
                    b[k].append(aname[k][i])
        
                #print(b[k])
                
                k=k+1
                driver.close()
                driver.switch_to_window(driver.window_handles[-1])


    driver.close()
    driver.quit()

    ## mysql insert ###
    for i in range(len(name_kor)):
        for j in range(len(b[i])):
            cursor.execute("INSERT INTO "+table_name+"(name_kor, belong,academy,academy_period) values( %s,%s,%s,%s);",(name_kor[i],belong,b[i][j],None))
    connect.commit()
    
    
