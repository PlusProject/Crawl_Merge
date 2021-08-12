from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
import pymysql

def scholar(connect, cursor, table_name, driver_path):

    wd=webdriver.Chrome(executable_path=driver_path)

    CHONNAMURLLIST=["http://www.cnuh.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=CV","http://www.cnuh.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=CS","https://www.cnuhch.com/medical/info/dept.cs?act=view&mode=doctorList&deptCd=PECV"]
    for urlitem in CHONNAMURLLIST:
        time.sleep(2)
        wd.get(urlitem)
        doctorlist=wd.find_elements_by_css_selector("#contents > div.sectionArea > ul > li > div > div.doctor > dl > dd.lkList > ul > li.intro > a > span")

        for i in range(len(doctorlist)):
            try:
                wd.get(urlitem)
                time.sleep(2)
                doctorlist = wd.find_elements_by_css_selector("#contents > div.sectionArea > ul > li > div > div.doctor > dl > dd.lkList > ul > li.intro > a > span")
                button=doctorlist[i]
                button.click()
                time.sleep(2)

                # 논문 쿼리: name, belong, pname만
                # detail01
                name_kor=wd.find_element_by_css_selector("#contents > div.doctorIntro > div.introHeader > div > dl > dt").text
                belong="전남대학교병원"
                link=wd.current_url

                # detail02: beautifulsoup 사용
                raw = requests.get(link)
                html = BeautifulSoup(raw.text, "html.parser")
                # 논문 이름 순회
                pname=""
                if (name_kor=="정인석"):
                    pnamelist = html.select("#introDetail02 > div:nth-child(1) > dl > dd:nth-child(6) > span.date")
                elif(name_kor=="정명호"):
                    continue
                else:
                    pnamelist = html.select("#introDetail02 > div:nth-child(1) > dl > dd > span.txt")
                for j in pnamelist:
                    # 각 논문 이름
                    try:
                        temppname=j.text.strip()
                        # ./,/-/로 단어들 구분하여 리스트 저장. 길이가 가장 긴 것이 논문 제목.
                        # 아닌 경우 예외 처리 필요. "그 외" , ..
                        temppnamelist=re.split("[.;,]",temppname)
                        ret=0
                        # 그 외
                        for string in temppnamelist:
                            if(ret<len(string)):
                                temp=string
                                ret=len(temp)
                        if ((temp!='')&('그 외' not in temp)):
                            # 숫자인지 아닌지
                            # 만약 첫번째 글자가 숫자라면 해당 글 제외하고, span.date에서 추가하기.
                            pname=temp
                            cursor.execute("INSERT INTO " + table_name + "(name_kor, belong, pname)values (%s, %s, %s)", (name_kor, belong, pname))
                            connect.commit()
                    except:
                        continue
            except:
                pass
    
    wd.close()
    wd.quit()
