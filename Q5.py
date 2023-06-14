search_k = input("크롤링할 키워드를 입력해주세요.:")
count_v = int(input("크롤링할 영상의 수를 입력해주세요:"))
count_c = int(input("크롤링할 댓글의 수를 입력해주세요:"))
save_point = input("결과 파일을 저장할 폴더명을 작성하세요.(예:c:\\data\\):")
r_save_point = f'{save_point}\{search_k}'

import pandas as pd 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

os.makedirs(f'{r_save_point}')
os.chdir(f'{r_save_point}')

##
path = "C:\Temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("http://youtube.com")
time.sleep(1)
search_bar = driver.find_element(By.NAME, "search_query")
search_bar.send_keys(search_k)
search_bar.submit()
time.sleep(1)
for _ in range(int(count_v / 5)+1):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.END)
    time.sleep(1)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

vds = []
soup = BeautifulSoup(driver.page_source, 'html.parser')
vd_rends = soup.find_all("ytd-video-renderer", class_="style-scope ytd-item-section-renderer")
for vd_r in vd_rends:
    v = vd_r.find("ytd-thumbnail", class_="style-scope ytd-video-renderer").find("a", class_="yt-simple-endpoint inline-block style-scope ytd-thumbnail").get("href")
    vds.append(v)
v_cnt = 0
nicks = []
cmts = []
dates = []
urls = []
v_no = []
c_no = []

for vd in vds:
    if (vd.startswith("/shorts")):
        continue
    driver.get("http://youtube.com" + vd)
    time.sleep(1)
    v_cnt += 1
    c_cnt = 0
    scroll_cnt = 0
    while len(cmts) < count_c * count_v:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        cmt_elements = soup.find_all("ytd-comment-thread-renderer")
        if (scroll_cnt == 3) & (len(cmt_elements) < count_c):
            v_cnt -= 1
            break
        for cmt_box in cmt_elements:
            if c_cnt >= count_c:
                break
            if len(cmt_elements) >= count_c:
                cmt_detail = cmt_box.find('ytd-comment-renderer').find('div', id='body').find('div', id='main')
                nicks.append(cmt_detail.find('div', id='header').find('div', id='header-author').find('h3').get_text().strip())
                dates.append(cmt_detail.find('div', id='header').find('div', id='header-author').find('yt-formatted-string', class_='published-time-text style-scope ytd-comment-renderer').get_text().strip())
                cmts.append(cmt_detail.find('div', id='comment-content').get_text().strip().replace("간략히", "").replace("자세히 보기", ""))
                urls.append("http://youtube.com" + vd)
                v_no.append(v_cnt)
                c_no.append(c_cnt)
                c_cnt += 1
        if c_cnt >= count_c:
            break
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        scroll_cnt += 1
    if (v_cnt-1 == count_v):
        break
        
df = pd.DataFrame()
df['영상번호'] = v_no
df['댓글번호'] = c_no
df['작성자'] = nicks
df['작성일자'] = dates
df['내용'] = cmts
df['url'] = urls
df.to_excel(f'{r_save_point}.xlsx')
df.to_csv(f'{r_save_point}.csv', encoding="utf-8-sig")
f = open(f'{r_save_point}.txt', 'a',encoding='UTF-8')
for i in range(len(v_no)):
    f.write(f'{str(v_no[i])}번째 영상의 {str(c_no[i]+1)}번째 댓글입니다. ~~\n')
    f.write(f'1.작성자: {nicks[i]}\n')
    f.write(f'2.작성일: {dates[i]}\n')
    f.write(f'3.댓글내용: {cmts[i]}\n')
    f.write(f'4.영상url: {urls[i]}\n\n')
f.close()
print("Finish")