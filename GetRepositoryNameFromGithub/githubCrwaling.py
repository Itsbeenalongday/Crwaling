import requests
from bs4 import BeautifulSoup as bs
import contextlib
 
# HTTP GET request
req = requests.get('https://github.com/Itsbeenalongday?tab=repositories')

# html file source
html = req.text

# beautiful soup는 html를 python 객체로 변환하는 데 도움을 준다.
# 첫 인자는 html file이름이고 두 번째 인자는 어떤 parser를 이용할지 명시
# 찾아보니 python 내장으로 html parser가 있더라~~
soup = bs(html, 'html.parser')

# soup객체에서 이제 자신이 원하는 정보를 추출하면 된다.
# css selector를 이용하는 select를 메소드를 사용하자

repos = soup.select('h3 > a')

path = '/Users/koominsoo/Desktop/workspace/crwaling/repos.txt'
with open(path, 'w') as f:
  with contextlib.redirect_stdout(f):
    for repo in repos:
      print(repo.text)