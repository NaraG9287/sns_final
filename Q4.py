search_ = input("검색어를 입력해주세요.:")
search_k = f'{search_} filetype:pdf'
count = int(input("몇 건의 pdf 파일을 저장할까요?:"))
save_point = input("결과 파일을 저장할 경로를 입력해주세요.(예:c:\\data\\):")

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import requests

os.makedirs(f'{save_point}\{search_}')
os.chdir(f'{save_point}\{search_}')
path = "C:\Temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("http://google.co.kr")

search_bar = driver.find_element(By.NAME, 'q')
search_bar.send_keys(search_k)
search_bar.submit()
time.sleep(1)

cnt = 0
error = 0
while True:
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.send_keys(Keys.END)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    urls = soup.find_all('a')
    
    for url in urls:
        try:
            if url.get('href').endswith('.pdf'):
                pdf_name = os.path.join(f'{save_point} - {search_k} \\ {str(cnt)}.pdf')
                response = requests.get(url.get('href'))
                with open(pdf_name, 'wb') as f:
                    f.write(response.content)
                print(f'{str(cnt+1)}번째 pdf파일 다운로드 성공')
                cnt += 1
                if cnt == count:
                    break
        except:
            error += 1
    if cnt == count:
        break
    try:
        driver.find_element(By.ID, 'pnnext').click()
    except:
        print("no more pages")
        break
    time.sleep(1)
print("Finish")