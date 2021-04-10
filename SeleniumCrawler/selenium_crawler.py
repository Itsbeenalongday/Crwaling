from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from konfig import Config
from bs4 import BeautifulSoup
from time import sleep
import contextlib

config = Config('../conf.ini')
path = config.get_map("path")
user_info = config.get_map("user")

driver = webdriver.Chrome(path['DRIVER_PATH'])

# 웹 자원 로드를 위해 3초까지 기다려준다.
driver.implicitly_wait(3)

# github에 로그인하기

driver.get('https://github.com/login')

driver.find_element_by_id('login_field').send_keys(user_info['ID'])
driver.find_element_by_id('password').send_keys(user_info['PASSWD'])

driver.find_element_by_name('commit').click()

driver.implicitly_wait(3)

driver.get('https://github.com/' + user_info['NAME'])

# page의 모든 엘레멘트 가져오기

driver.find_element_by_css_selector('#js-pjax-container > div.mt-4.position-sticky.top-0.d-none.d-md-block.color-bg-primary.width-full.border-bottom.color-border-secondary > div > div > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div > nav > a:nth-child(2)').click()

#id 속성이 user-repositories-list인 element가 리턴될때까지 10초간 기다리는 것 입니다. 만약 10초 전에 page가 로딩되고 element가 실행된다면 EC는 true를 반환하게 됩니다.

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user-repositories-list")))

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

repos = []

for repo in soup.find_all("a", itemprop="name codeRepository"):
  repos.append(repo.text.strip().lstrip('\n'))

sleep(5)

has_next_page = True

while has_next_page:
  pagination_buttons = driver.find_elements_by_css_selector('#user-repositories-list > div > div > a')
  for button in pagination_buttons:
    if(button.get_attribute('innerHTML') == "Previous" and len(pagination_buttons) == 1):
      print("END")
      has_next_page = False
      break
    if(button.get_attribute('innerHTML') == "Next"):
      print("go to next")
      button.click()
      driver.implicitly_wait(10)
      html = driver.page_source
      soup = BeautifulSoup(html, 'html.parser')
      for repo in soup.find_all("a", itemprop="name codeRepository"):
        repos.append(repo.text.strip().lstrip('\n'))

#driver.quit()

path = path['WORKING_PATH'] + '/SeleniumCrawler/repos.txt'
with open(path, 'w') as f:
  with contextlib.redirect_stdout(f):
    print("repos count: {count}개".format(count=len(repos)))
    for repo in repos:
      print(repo)

print('현재 레포지토리의 수는 {count}, repos.txt에 저장이 완료되었습니다'.format(count=len(repos)))

# URL에 접근하는 메소드,

# get('http://url.com')
# 페이지의 단일 element에 접근하는 메소드,

# find_element_by_name('HTML_name')
# find_element_by_id('HTML_id')
# find_element_by_xpath('/html/body/some/xpath')
# find_element_by_css_selector('#css > div.selector')
# find_element_by_class_name('some_class_name')
# find_element_by_tag_name('h1')
# 페이지의 여러 elements에 접근하는 메소드 등이 있다. (대부분 element 를 elements 로 바꾸기만 하면 된다.)

# find_elements_by_css_selector('#css > div.selector')
# 위 메소드들을 활용시 HTML을 브라우저에서 파싱해주기 때문에 굳이 Python와 BeautifulSoup을 사용하지 않아도 된다.

# 하지만 Selenium에 내장된 함수만 사용가능하기 때문에 좀더 사용이 편리한 soup객체를 이용하려면 driver.page_source API를 이용해 현재 렌더링 된 페이지의 Elements를 모두 가져올 수 있다.

# driver.page_source: 브라우저에 보이는 그대로의 HTML, 크롬 개발자 도구의 Element 탭 내용과 동일.

# requests 통해 가져온 req.text: HTTP요청 결과로 받아온 HTML, 크롬 개발자 도구의 페이지 소스 내용과 동일.

# 위 2개는 사이트에 따라 같을수도 다를수도 있습니다.
