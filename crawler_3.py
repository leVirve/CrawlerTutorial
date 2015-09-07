import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')

for article in articles:
    meta = article.find('div', 'title').find('a')

    title = meta.getText().strip()
    link = meta.get('href')
    push = article.find('div', 'nrec').getText()
    date = article.find('div', 'date').getText()
    author = article.find('div', 'author').getText()

    print(title, date, author, link)
