search_k = input('1. 크롤링할 키워드를 입력하세요.(예:고양이): ')
count = int(input('2. 크롤링할 건수는 몇건입니까?: '))
save_point = input("3.추출 결과를 저장할 폴더명을 입력하세요.(예:c:\\data\\):")

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests

os.makedirs(f'{save_point}\{search_k}')
os.chdir(f'{save_point}\{search_k}')
img_folder = os.path.join(f'{save_point}\{search_k}')
driver_path = "C:\Temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(driver_path)
driver.get(f"https://pixabay.com/ko/images/search/{search_k}/")
time.sleep(1)

cnt = 0
error = 0
while cnt < count:
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    before_height = driver.execute_script("return document.body.scrollHeight")
    after_height=0
    while after_height != before_height:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        after_height = driver.execute_script("return document.body.scrollHeight")
        before_height = after_height
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    all_img = soup.find_all('img')
    for img in all_img:
        try:
            img_url = img.get('src')
            img_name = str(cnt+1) + ".jpg"
            response = requests.get(img_url)
            with open(os.path.join(img_folder, img_name), 'wb') as f:
                f.write(response.content)
            cnt += 1
            print(str(cnt) + " - Downloading...")
            if cnt == count:
                break
        except:
            error += 1
        time.sleep(1)
    page = 1
    if cnt < count:
        page += 1
        next = f'https://pixabay.com/ko/images/search/{search_k}/?pagi={str(page)}'
        driver.get(next)

print("요청하신 데이터 추출이 성공적으로 끝났습니다.")