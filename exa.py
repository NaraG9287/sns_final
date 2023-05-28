
# Step 1. 각종 라이브러리 불러오기
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests as rq
import pyperclip
import time
import sys
import csv
import openpyxl
import pandas as pd
import xlwt

# 크롬 드라이버 자동 업데이트를 위함
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 최신 버전을 설치 후 서비스 객체를 만듦
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)



##########################################################################################

# Step 2. 각종 입력 받기
# search_k = input('공고명으로 검색할 키워드는 무엇입니까?: ')        # 키워드검색
# start_date = input('조회 시작일자 입력 (예: 2023/01/01) ')        # 시작일자 입력
# end_date = input('조회 종료일자 입력 (예: 2023/12/31) ')        # 종료일자 입력
# save_point = input('파일로 저장할 폴더 이름을 쓰세요 (예: c:\data\): ')

# f_name = input('검색 결과를 저장할 txt 파일경로와 이름을 지정하세요(예:c:\\data\\test_3.txt): ')
# fx_name = input('검색 결과를 저장할 xlsx 파일경로와 이름을 지정하세요(예:c:\\data\\test_3.xlsx): ')

# 웹 페이지 실행 시키기
driver.get("https://www.g2b.go.kr/index.jsp")
driver.implicitly_wait(60)
# 창을 최대화시킴
driver.maximize_window()




# Step 3. 웹 페이지에서 키워드 검색 하기.

# 검색어 입력
element = driver.find_element(By.CSS_SELECTOR, "#bidNm")
element.click()
time.sleep(0.5)
# element.send_keys(search_k)
element.send_keys("캠프")
driver.implicitly_wait(5)

# 조회 시작일자 입력
element = driver.find_element(By.CSS_SELECTOR, "#fromBidDt.w70")
element.click()
element.send_keys(Keys.CONTROL+'a')
time.sleep(0.5)
element.send_keys("2019/01/01")
driver.implicitly_wait(3)


# 조회 종료일자 입력
element = driver.find_element(By.CSS_SELECTOR, "#toBidDt.w70")
element.click()
element.send_keys(Keys.CONTROL+'a')
time.sleep(0.5)
element.send_keys("2019/04/20")

# 검색 버튼 클릭
element = driver.find_element(By.CSS_SELECTOR, ".btn_dark")
element.click()
time.sleep(0.5)    ##여기까진 ㅇㅋ
##########################################################################################
# Step 4. 현재 페이지에 있는 내용을 화면에 출력하기

time.sleep(1)

html = driver.page_source
soup = bs(html, 'html.parser')
content_table = soup.find('table',class_='table_list_tbidTbl table_list')

# 학습목표 1: 특정 항목들을 분리해서 추출하기
# row(가로줄), col(세로줄) 들로 데이터 저장
# {n}번째 공고내용을 추출합니다~~~~
# 1. 업무 : 
# 2. 공고번호-차수 : 
# 3. 분류 : 
# 4. 공고명 : 
# 5. URL 주소 : 
# 6. 공고기관 : 
# 7. 수요기관 : 
# 8. 계약방법 : 
# 9. 입력일시(입찰마감일시) : 
# 11. 공동수급 : 
# 12. 투찰여부 : 



##########################################################################################
# Step 5. 각 항목별로 분리하여 추출하고 변수에 할당하기
no = 1
no2 =[ ]            # 번호
blogs2 = [ ]        # 제목
nae2 = [ ]          # 내용
date2 = [ ]         # 작성일자
nick_n2 = [ ]       # 블로그네임

for row in range(1, 11, 1):
    for col in range(1, 11, 1):
        no2.append(no)
        print('1. 번호:',no)
        blog_list = soup.find('li',id=f'sp_blog_{row}')
        
        blogs = blog_list.find('a', 'api_txt_lines total_tit').get_text()
        blogs2.append(blogs)
        print('2. 제목: ',blogs.strip())
        
        nae = blog_list.find('div','api_txt_lines dsc_txt').get_text()
        nae2.append(nae)
        print('3. 내용: ',nae.strip())
        
        date = blog_list.find('span','sub_time sub_txt').get_text()
        date2.append(date)
        print('4. 작성일자: ',date.strip())    
        nick_n = blog_list.find('a','sub_txt sub_name').get_text()
        nick_n2.append(nick_n)
        print('5. 블로그네임: ',nick_n.strip())
        print('====================================================================')
        
        no += 1                             ## 여기 까지 ㅇㅋ

    """
##########################################################################################
# 학습목표 2: 분리 수집된 데이터를 데이터 프레임으로 만들어서 
# csv , xls 형식으로 저장하기

# 출력 결과를 표(데이터 프레임) 형태로 만들기

dataData = pd.DataFrame()
dataData['번호']=no2
dataData['제목']=blogs2
dataData['내용']=nae2
dataData['작성일자']=date2
dataData['블로그네임']=nick_n2

# csv 형태로 저장하기
dataData.to_csv(fc_name, encoding="utf-8-sig")
print(f" csv 파일 저장 경로: {fc_name}")

# 엑셀 형태로 저장하기
dataData.to_excel(fx_name)
print(f" xlsx 파일 저장 경로: {fx_name}")

# text출력
page = 0

for Num in range(1, 12, 1):
    f = open(f'{f_name}', 'a')
    post_elems = driver.find_elements(By.CSS_SELECTOR, f"#sp_blog_{Num}")
    # 블로그 제목 출력
    post_titles = map(lambda post: post.find_element(By.CSS_SELECTOR, ".api_txt_lines.total_tit").text, post_elems)
    post_nae = map(lambda post: post.find_element(By.CSS_SELECTOR, ".api_txt_lines.dsc_txt").text, post_elems)
    post_dates = map(lambda post: post.find_element(By.CSS_SELECTOR, ".sub_time.sub_txt").text, post_elems)
    post_writter = map(lambda post: post.find_element(By.CSS_SELECTOR, ".sub_txt.sub_name").text, post_elems)
#    print(f'1. 번호: {Num}')
#    print(f'2. 제목: {", ".join(post_titles)}')
#    print(f'3. 내용:  {", ".join(post_nae)}')
#    print(f'4. 작성일자:  {", ".join(post_dates)}')
#    print(f'5. 블로그닉네임:  {", ".join(post_writter)}')
#    print('------------------------------------------------------------------------------------------------------------')

    # txt 형식 저장
    post_titles2 = map(lambda post: post.find_element(By.CSS_SELECTOR, ".api_txt_lines.total_tit").text, post_elems)
    post_nae2 = map(lambda post: post.find_element(By.CSS_SELECTOR, ".api_txt_lines.dsc_txt").text, post_elems)
    post_dates2 = map(lambda post: post.find_element(By.CSS_SELECTOR, ".sub_time.sub_txt").text, post_elems)
    post_writter2 = map(lambda post: post.find_element(By.CSS_SELECTOR, ".sub_txt.sub_name").text, post_elems)

    f.write(f'{Num}번째 공고내용을 추출합니다~~~~\n')
    f.write(f'1. 업무: {", ".join(post_titles2)}\n')
    f.write(f'2. 공고번호-차수: {", ".join(post_titles2)}\n')
    f.write(f'3. 분류:  {", ".join(post_nae2)}\n')
    f.write(f'4. 공고명:  {", ".join(post_dates2)}\n')
    f.write(f'5. URL 주소:  {", ".join(post_writter2)}\n')
    f.write(f'6. 공고기관:  {", ".join(post_writter2)}\n')
    f.write(f'7. 수요기관:  {", ".join(post_writter2)}\n')
    f.write(f'8. 계약방법:  {", ".join(post_writter2)}\n')
    f.write(f'9. 입력일시(입찰마감일시):  {", ".join(post_writter2)}\n')
    f.write(f'11. 공동수급:  {", ".join(post_writter2)}\n')
    f.write(f'12. 투찰여부:  {", ".join(post_writter2)}\n')
    f.write('------------------------------------------------------------------------------------------------------------\n')

    page += 1
f.close

print(f" txt 파일 저장 경로: {f_name}")

# print("END")
 """

input()