
save_file_name = 'Q2_20181517박성빈'

import urllib.parse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

# 크롬 드라이버 자동 업데이트를 위함
from webdriver_manager.chrome import ChromeDriverManager

search_k = input('1. 크롤링할 키워드는 무엇입니까?(예: 여행): ')
add_k = list(input('2. 결과에서 반드시 포함하는 단어를 입력하세요(예: 국내, 바닷가)\n(여러개일 경우 , 로 구분해서 입력하고 없으면 엔터 입력하세요): ').split(','))
add_k2 = ' '.join(['%2B' + urllib.parse.quote(keyword1) for keyword1 in add_k])
mia_k = list(input('3. 결과에서 제외활 단어를 입력하세요(예: 분양권, 해외)\n(여러개일 경우 , 로 구분해서 입력하고 없으면 엔터 입력하세요): ').split(','))
mia_k2 = ' '.join(['-' + keyword2 for keyword2 in mia_k])
search_kK = search_k + ' ' + add_k2 + ' ' + mia_k2
start_date = input('4. 조회 시작일자 입력(예: 2017-01-01): ')
end_date = input('5. 조회 종료일자 입력(예: 2017-12-31): ')
count_data = int(input('6. 크롤링 할 건수는 몇건입니까?: '))
save_point = input('7. 파일을 저장할 폴더명만 쓰세요: (예: c:\\temp\\): ')

# 크롬 드라이버 최신 버전을 설치 후 서비스 객체를 만듦
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 웹 페이지 오픈을 위한 옵션들
# ５초까지는 로딩을 기다림
driver.implicitly_wait(5)
# 창을 최대화시킴
driver.maximize_window()

driver.get(f'https://search.naver.com/search.naver?where=blog&query={search_kK}&sm=tab_opt&nso=so:r,p:from{start_date}to{end_date}')
driver.implicitly_wait(60)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Step 5. 각 항목별로 분리하여 추출하고 변수에 할당하기
no = 1
no2 =[ ]            # 번호
blogs2 = [ ]        # 제목
nae2 = [ ]          # 내용
date2 = [ ]         # 작성일자
nick_n2 = [ ]       # 블로그네임
link2 = [ ]

for i in range(1, count_data+1, 1):
    no2.append(no)
    print('1. 번호:',no)
    blog_list = soup.find('li',id=f'sp_blog_{i}')

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
    link = driver.find_element(By.CSS_SELECTOR, '.total_area > a').get_attribute('href')
    link2.append(link)
    print('6. 블로그링크: ',link.strip())
    print('====================================================================')

    no += 1
##########################################################################################
# 학습목표 2: 분리 수집된 데이터를 데이터 프레임으로 만들어서 
# csv , xls 형식으로 저장하기

# 출력 결과를 표(데이터 프레임) 형태로 만들기

import pandas as pd

dataData = pd.DataFrame()
dataData['블로그주소']=link2
dataData['작성자닉네임']=nick_n2
dataData['작성일자']=date2
dataData['블로그내용']=nae2

# csv 형태로 저장하기
dataData.to_csv(f'{save_point+save_file_name}.csv', encoding="utf-8-sig")
print(f" csv 파일 저장 경로: {save_point+save_file_name}.csv")

# 엑셀 형태로 저장하기
import xlwt   # pip install xlwt 실행 후 수행
dataData.to_excel(f'{save_point+save_file_name}.xlsx')
print(f" xlsx 파일 저장 경로: {save_point+save_file_name}.xlsx")

# text출력
page = 0

for Num in range(1, count_data+1, 1):
    f = open(f'{save_point+save_file_name}.txt', 'a')    
    post_elems = driver.find_elements(By.CSS_SELECTOR, f"#sp_blog_{Num}")
    # 블로그 제목 출력
    post_nae = map(lambda post: post.find_element(By.CSS_SELECTOR, ".api_txt_lines.dsc_txt").text, post_elems)
    post_dates = map(lambda post: post.find_element(By.CSS_SELECTOR, ".sub_time.sub_txt").text, post_elems)
    post_writter = map(lambda post: post.find_element(By.CSS_SELECTOR, ".sub_txt.sub_name").text, post_elems)
    post_link = map(lambda post: post.find_element(By.CSS_SELECTOR, ".total_area > a").get_attribute('href'), post_elems)

    # txt 형식 저장
    post_nae2 = map(lambda post: post.find_element(By.CSS_SELECTOR, ".api_txt_lines.dsc_txt").text, post_elems)
    post_dates2 = map(lambda post: post.find_element(By.CSS_SELECTOR, ".sub_time.sub_txt").text, post_elems)
    post_writter2 = map(lambda post: post.find_element(By.CSS_SELECTOR, ".sub_txt.sub_name").text, post_elems)
    post_link2 = map(lambda post: post.find_element(By.CSS_SELECTOR, ".total_area > a").get_attribute('href'), post_elems)

    f.write(f'총 {count_data} 건 중 {Num} 번째 블로그 데이터를 수집합니다===============\n')
    f.write(f'1. 블로그 주소:  {", ".join(post_link2)}\n')
    f.write(f'2. 작성자 닉네임:  {", ".join(post_writter2)}\n')
    f.write(f'3. 작성일자:  {", ".join(post_dates2)}\n')
    f.write(f'4. 블로그 내용:  {", ".join(post_nae2)}\n')

    page += 1
f.close

print(f" txt 파일 저장 경로: {save_point+save_file_name}.txt")

input()

print("END")