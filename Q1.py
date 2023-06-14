# Step 0. 각종 입력 받기
search_k = input('공고명으로 검색할 키워드는 무엇입니까?: ')        # 키워드검색
start_date = input('조회 시작일자 입력 (예: 2023/01/01) ')        # 시작일자 입력
end_date = input('조회 종료일자 입력 (예: 2023/12/31) ')        # 종료일자 입력
save_point = input('파일로 저장할 폴더 이름을 쓰세요 (예: c:\data): ')
f_name = 'Q1_20181517박성빈'
r_save_point = f'{save_point}\{f_name}'


# Step 1. 각종 라이브러리 불러오기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 크롬 드라이버 자동 업데이트를 위함
from webdriver_manager.chrome import ChromeDriverManager

# 크롬 드라이버 최신 버전을 설치 후 서비스 객체를 만듦
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 웹 페이지 실행 시키기
url = "https://www.g2b.go.kr/index.jsp"
driver.get(url)
driver.implicitly_wait(60)
# 창을 최대화시킴
driver.maximize_window()

# google에 my user agent
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}


# Step 3. 웹 페이지에서 키워드 검색 하기.

# 검색어 입력
element = driver.find_element(By.CSS_SELECTOR, "#bidNm")
element.click()
time.sleep(0.5)
element.send_keys(search_k)
driver.implicitly_wait(5)

# 조회 시작일자 입력
element = driver.find_element(By.CSS_SELECTOR, "#fromBidDt.w70")
element.click()
element.send_keys(Keys.CONTROL+'a')
time.sleep(0.5)
element.send_keys(start_date)
driver.implicitly_wait(3)


# 조회 종료일자 입력
element = driver.find_element(By.CSS_SELECTOR, "#toBidDt.w70")
element.click()
element.send_keys(Keys.CONTROL+'a')
time.sleep(0.5)
element.send_keys(end_date)

# 검색 버튼 클릭
element = driver.find_element(By.CSS_SELECTOR, ".btn_dark")
element.click()
time.sleep(0.5)

driver.switch_to.frame('sub')
driver.switch_to.frame('main')
nara_table = driver.find_element(By.CLASS_NAME, 'table_list_tbidTbl')
nara_tbody = nara_table.find_element(By.TAG_NAME, 'tbody')
nara_rows = nara_tbody.find_elements(By.TAG_NAME,'tr')

no = 1
no2 =[ ]            # 번호
업무 = [ ]
공고번호_차수 = [ ]
분류 = [ ]
공고명 = [ ]
공고링크 = [ ]
공고기관 = [ ]
수요기관 = [ ]
계약방법 = [ ]
입력일시 = [ ]
공동수급 = [ ]
투찰여부 = [ ]

for col, row in enumerate(nara_rows):
    content = row.find_elements(By.TAG_NAME, 'td')
    no2.append(no)
    업무.append(content[0].text)
    공고번호_차수.append(content[1].text)
    분류.append(content[2].text)
    nara_link = content[3].find_element(By.TAG_NAME, 'div').find_element(By.TAG_NAME, 'a')
    공고명.append(nara_link.text)
    공고링크.append(nara_link.get_attribute("href"))
    공고기관.append(content[4].text)
    수요기관.append(content[5].text)
    계약방법.append(content[6].text)
    입력일시.append(content[7].text)
    공동수급.append(content[8].text)
    투찰여부.append(content[9].text)
    no += 1




df = pd.DataFrame()
df['용역']=업무
df['공고번호-차수']=공고번호_차수
df['분류']=분류
df['공고명']=공고명
df['URL']=공고링크
df['공고기관']=공고기관
df['수요기관']=수요기관
df['계약방법']=계약방법
df['입력일시']=입력일시
df['공동수급']=공동수급
df['투찰여부']=투찰여부

f = open(f'{r_save_point}.txt', 'a',encoding='UTF-8')
for i in range(len(no2)):
    f.write(f'{str(no2[i])}번째 공고내용입니다. ~~~~\n')
    f.write(f'1.업무: {업무[i]}\n')
    f.write(f'2.공고번호-차수: {공고번호_차수[i]}\n')
    f.write(f'3.분류: {분류[i]}\n')
    f.write(f'4.공고명: {공고명[i]}\n')
    f.write(f'5.URL: {공고링크[i]}\n')
    f.write(f'6.공고기관: {공고기관[i]}\n')
    f.write(f'7.수요기관: {수요기관[i]}\n')
    f.write(f'8.계약방법: {계약방법[i]}\n')
    f.write(f'9.입력일시(입찰마감일시): {입력일시[i]}\n')
    f.write(f'10.공동수급: {공동수급[i]}\n')
    f.write(f'11.투찰여부: {투찰여부[i]}\n')
f.close()
df.to_csv(f'{r_save_point}.csv', encoding="utf-8-sig") 
df.to_excel(f'{r_save_point}.xlsx')
print("Finish")


input()