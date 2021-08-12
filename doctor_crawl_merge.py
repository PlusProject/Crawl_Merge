from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pymysql
import requests
import re

#중앙대학교병원 - CAU
import cau_academy, cau_doctor
#충북대학교병원 - CBN
import cbn_doctor, cbn_academy
#동아대학교병원 - DAMC
import dongA_doctor, dongA_academy, dongA_scholar
#강릉아산병원-GNAH
import gnah_doctor, gnah_academy
#계명대학교동산병원-DSMC
import keimyung_doctor, keimyung_academy, keimyung_scholar
#삼성서울-SAMSUNG
import 삼성, 삼성논문, 삼성학회
#연세대학교원주세브란스기독병원-YWMC
import wonjuSeverance_doctor, wonjuSeverance_academy
#경희대학교병원-KHUH
import khuh_doctor, khuh_academy
#전남대학교병원-CHONNAM
import chonnam_doctor, chonnam_academy, chonnam_scholar
#충남대학교병원-CNUH
import chungnam_doctor, chungnam_academy
#부산대학교병원-PNUHM
import pnuhm_doctor, pnuhm_academy
#강북삼성병원-KBSMC
import kbsmc_doctor, kbsmc_academy, kbsmc_scholar
#건국대학교-KUH
import kuh_doctor, kuh_academy, kuh_scholar, kuh_engName
#양산/어린이 부산대학교-PNUH
import pnuh_doctor, pnuh_academy, pnuh_scholar, pnuh_engName
#분당서울대학교병원-SNUBH
import snubh_doctor, snubh_academy, snubh_scholar, snubh_engName
#삼성창원병원-CWSMC
import cwsmc_doctor, cwsmc_academy, cwsmc_engName
#인제대학교병원-INJE
import inje_doctor, inje_academy, inje_scholar
#카톨릭대학교 대전성모병원-CMCDJ
import cmcdj_doctor, cmcdj_academy, cmcdj_scholar
#카톨릭대학교 인천성모병원-CMCISM
import cmcism_doctor, cmcism_academy, cmcism_scholar


host = 'localhost'
user = 'root'
passwd = 'Pas1324680@'
db = 'hospital_crawl'
driver_path = './chromedriver'

doctor_table = 'doctor'
academy_table = 'academy'
scholar_table = 'scholar'
engName_table = 'engName'

conn = pymysql.connect(
    user =user,
    passwd = passwd,
    db = db,
    host = host,
    charset = 'utf8mb4'
)
cursor = conn.cursor()

#의료진 Table
cursor.execute("DROP TABLE IF EXISTS "+doctor_table)
conn.commit()

sql = '''CREATE TABLE '''+doctor_table+'''(
name_kor VARCHAR(10) NOT NULL,
belong VARCHAR(30),
major mediumtext,
education mediumtext,
career mediumtext,
link mediumtext,
hospital_code VARCHAR(6)
)'''
cursor.execute(sql)
conn.commit()

#학회 Table
cursor.execute("DROP TABLE IF EXISTS "+academy_table)
conn.commit()

sql = '''CREATE TABLE '''+academy_table+'''(
name_kor VARCHAR(10) NOT NULL,
belong VARCHAR(30),
academy mediumtext,
academy_period mediumtext
)'''
cursor.execute(sql)
conn.commit()

#논문 Table
cursor.execute("DROP TABLE IF EXISTS "+scholar_table)
conn.commit()

sql = '''CREATE TABLE '''+scholar_table+'''(
name_kor VARCHAR(10) NOT NULL,
belong VARCHAR(30),
pname mediumtext
)'''
cursor.execute(sql)
conn.commit()

#영어 이름 Table
cursor.execute("DROP TABLE IF EXISTS "+engName_table)
conn.commit()

sql = '''CREATE TABLE '''+engName_table+'''(
name_kor VARCHAR(45) NOT NULL,
belong VARCHAR(45),
name_eng VARCHAR(45)
)'''
cursor.execute(sql)
conn.commit()

#======크롤링 시작=======
"""
#중앙대학교병원 - CAU
cau_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("중앙대학교병원 - 의료진 성공")
cau_academy.academy(conn, cursor, academy_table, driver_path)
print("중앙대학교병원 - 학회 성공")

#충북대학교병원 - CBN
cbn_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("충북대학교병원 - 의료진 성공")
cbn_academy.academy(conn, cursor, academy_table, driver_path)
print("충북대학교병원 - 학회 성공")

#동아대학교병원 - DAMC
dongA_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("동아대학교병원 - 의료진 성공")
dongA_academy.academy(conn, cursor, academy_table, driver_path)
print("동아대학교병원 - 학회 성공")
dongA_scholar.scholar(conn, cursor, scholar_table, driver_path)
print("동아대학교병원 - 논문 성공")

#강릉아산병원-GNAH
gnah_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("강릉아산병원 - 의료진 성공")
gnah_academy.academy(conn, cursor, academy_table, driver_path)
print("강릉아산병원 - 학회 성공")

#계명대학교동산병원-DSMC
keimyung_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("계명대학교동산병원 - 의료진 성공")
keimyung_academy.academy(conn, cursor, academy_table, driver_path)
print("계명대학교동산병원 - 학회 성공")
keimyung_scholar.scholar(conn, cursor, scholar_table, driver_path)
print("계명대학교동산병원 - 논문 성공")

#삼성서울-SAMSUNG
삼성.doctor(conn, cursor, doctor_table, driver_path)
print("삼성서울 - 의료진 성공")
삼성학회.academy(conn, cursor, doctor_table, academy_table, driver_path)
print("삼성서울 - 학회 성공")
삼성논문.scholar(conn, cursor, doctor_table, scholar_table, driver_path)
print("삼성서울 - 논문 성공")

#연세대학교원주세브란스기독병원-YWMC
wonjuSeverance_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("연세대학교원주세브란스기독병원 - 의료진 성공")
wonjuSeverance_academy.academy(conn, cursor, academy_table, driver_path)
print("연세대학교원주세브란스기독병원 - 학회 성공")

#경희대학교병원-KHUH
khuh_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("경희대학교병원 - 의료진 성공")
khuh_academy.academy(conn, cursor, academy_table, driver_path)
print("경희대학교병원 - 학회 성공")

#전남대학교병원-CHONNAM
chonnam_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("전남대학교병원 - 의료진 성공")
chonnam_academy.academy(conn, cursor, academy_table, driver_path)
print("전남대학교병원 - 학회 성공")
chonnam_scholar.scholar(conn, cursor, scholar_table, driver_path)
print("전남대학교병원 - 논문 성공")

#충남대학교병원-CNUH
chungnam_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("충남대학교병원 - 의료진 성공")
chungnam_academy.academy(conn, cursor, academy_table, driver_path)
print("충남대학교병원 - 학회 성공")

#부산대학교병원-PNUHM
pnuhm_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("부산대학교병원 - 의료진 성공")
pnuhm_academy.academy(conn, cursor, academy_table, driver_path)
print("부산대학교병원 - 학회 성공")

#강북삼성병원-KBSMC
kbsmc_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("강북삼성병원 - 의료진 성공")
kbsmc_academy.academy(conn, cursor, academy_table, doctor_table, driver_path)
print("강북삼성병원 - 학회 성공")
kbsmc_scholar.scholar(conn, cursor, scholar_table, doctor_table, driver_path)
print("강북삼성병원 - 논문 성공")
"""
#건국대학교-KUH
kuh_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("건국대학교 - 의료진 성공")
kuh_academy.academy(conn, cursor, academy_table, doctor_table, driver_path)
print("건국대학교 - 학회 성공")
kuh_scholar.scholar(conn, cursor, scholar_table, doctor_table, driver_path)
print("건국대학교 - 논문 성공")
kuh_engName.engName(conn, cursor, engName_table, doctor_table, driver_path)
print("건국대학교 - 영어이름 성공")

#양산/어린이 부산대학교-PNUH
pnuh_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("양산/어린이 부산대학교 - 의료진 성공")
pnuh_academy.academy(conn, cursor, academy_table, doctor_table, driver_path)
print("양산/어린이 부산대학교 - 학회 성공")
pnuh_scholar.scholar(conn, cursor, scholar_table, doctor_table, driver_path)
print("양산/어린이 부산대학교 - 논문 성공")
pnuh_engName.engName(conn, cursor, engName_table, doctor_table, driver_path)
print("양산/어린이 부산대학교 - 영어이름 성공")
"""
#분당서울대학교병원-SNUBH
snubh_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("분당서울대학교병원 - 의료진 성공")
snubh_academy.academy(conn, cursor, academy_table, doctor_table, driver_path)
print("분당서울대학교병원 - 학회 성공")
snubh_scholar.scholar(conn, cursor, scholar_table, doctor_table, driver_path)
print("분당서울대학교병원 - 논문 성공")
snubh_engName.engName(conn, cursor, engName_table, doctor_table, driver_path)
print("분당서울대학교병원 - 영어이름 성공")

#삼성창원병원-CWSMC
cwsmc_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("삼성창원병원 - 의료진 성공")
cwsmc_academy.academy(conn, cursor, academy_table, doctor_table, driver_path)
print("삼성창원병원 - 학회 성공")
cwsmc_engName.engName(conn, cursor, engName_table, doctor_table, driver_path)
print("삼성창원병원 - 영어이름 성공")

#인제대학교병원-INJE
inje_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("인제대학교병원 - 의료진 성공")
inje_academy.academy(conn, cursor, academy_table, doctor_table, driver_path)
print("인제대학교병원 - 학회 성공")
inje_scholar.scholar(conn, cursor, scholar_table, doctor_table, driver_path)
print("인제대학교병원 - 논문 성공")

#가톨릭대학교 대전성모병원-CMCDJ
cmcdj_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("가톨릭대학교 대전성모병원 - 의료진 성공")
cmcdj_academy.academy(conn, cursor, academy_table, doctor_table, driver_path)
print("가톨릭대학교 대전성모병원 - 학회 성공")
cmcdj_scholar.scholar(conn, cursor, scholar_table, doctor_table, driver_path)
print("가톨릭대학교 대전성모병원 - 논문 성공")

#가톨릭대학교 인천성모병원-CMCISM
cmcism_doctor.doctor(conn, cursor, doctor_table, driver_path)
print("가톨릭대학교 인천성모병원 - 의료진 성공")
cmcism_academy.academy(conn, cursor, academy_table, doctor_table, driver_path)
print("가톨릭대학교 인천성모병원 - 학회 성공")
cmcism_scholar.scholar(conn, cursor, scholar_table, doctor_table, driver_path)
print("가톨릭대학교 인천성모병원 - 논문 성공")
"""
#PK, FK 추가하는 코드

conn.close()
print("end")


