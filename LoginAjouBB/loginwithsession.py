import requests
from konfig import Config
from bs4 import BeautifulSoup as bs

config = Config('../conf.ini')
login_info = config.get_map("user")

user_info = {
  'login': login_info['ID'],
  'password': login_info['PASSWD']
}

with requests.Session() as session:
    login_req = session.post('https://sso.ajou.ac.kr/jsp/sso/ip/login_meta_form.jsp', data=user_info)
    
    if login_req.status_code != 200:
      raise Exception('로그인 실패했습니다. 오류코드: {code} '.format(code=login_req.status_code))
    
    # js 로 생성하는 듯 하다 아무것도 안나옴..
    notices = session.get('https://eclass2.ajou.ac.kr/ultra/course')
    soup = bs(notices.text, 'html.parser')    
    subjects = soup.select('h4')
    print(subjects)

