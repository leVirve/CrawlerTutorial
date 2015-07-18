import requests
import urllib.parse
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'

NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a


def get_posts(url):
    posts = list()

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', 'r-ent')

    global control
    control = soup.find_all('div', 'pull-right')[0].find_all('a', 'btn')

    for article in articles:
        title_meta = article.find('div', 'title').find('a') or NOT_EXIST
        meta = article.find('div', 'meta')

        post = dict()
        post['link'] = title_meta.get('href', '')
        post['title'] = title_meta.string.strip()
        post['date'] = meta.find('div', 'date').string
        post['author'] = meta.find('div', 'author').string
        posts.append(post)

    return posts

control = None
pages = 5

page_url = url

for i in range(pages):
    posts = get_posts(page_url)
    prev_link = control[1]['href']
    page_url = urllib.parse.urljoin(url, prev_link)
    print(posts)
