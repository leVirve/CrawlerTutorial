import requests
import urllib.parse
from bs4 import BeautifulSoup

from utils import pretty_print

INDEX = 'https://www.ptt.cc/bbs/movie/index.html'
NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

control = None


def get_posts_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    global control
    control = soup.find('div', 'pull-right').find_all('a', 'btn')
    articles = soup.find_all('div', 'r-ent')

    posts = list()
    for article in articles:
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        posts.append({
            'title': meta.getText().strip(),
            'link': meta.get('href'),
            'push': article.find('div', 'nrec').getText(),
            'date': article.find('div', 'date').getText(),
            'author': article.find('div', 'author').getText(),
        })
    return posts


def get_pages(num):
    page_url = INDEX
    all_posts = list()
    for i in range(num):
        all_posts += get_posts_on_page(page_url)
        prev_link = control[1]['href']
        page_url = urllib.parse.urljoin(INDEX, prev_link)
    return all_posts


if __name__ == '__main__':
    pages = 5
    for post in get_pages(pages):
        pretty_print(post['push'], post['title'], post['date'], post['author'])
