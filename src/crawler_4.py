import requests
import urllib.parse
from bs4 import BeautifulSoup

from utils import pretty_print

INDEX = 'https://www.ptt.cc/bbs/movie/index.html'
NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a


def get_posts_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

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

    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[1].get('href')

    return posts, next_link


def get_pages(num):
    page_url = INDEX
    all_posts = list()
    for i in range(num):
        posts, link = get_posts_on_page(page_url)
        all_posts += posts
        page_url = urllib.parse.urljoin(INDEX, link)
    return all_posts


if __name__ == '__main__':
    pages = 1
    for post in get_pages(pages):
        pretty_print(post['push'], post['title'], post['date'], post['author'])
