import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')

for article in articles:
    title_meta = article.find('div', 'title').find('a')
    meta = article.find('div', 'meta')

    link = title_meta['href']
    title = title_meta.text
    date = meta.find('div', 'date').text
    author = meta.find('div', 'author').text

    print(title, date, author, link)
