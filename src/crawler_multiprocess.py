import time
import urllib.parse
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup


INDEX = 'https://www.ptt.cc/bbs/movie/index.html'
NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a


def get_posts_list(url):
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


def get_paged_meta(page):
    page_url = INDEX
    all_posts = list()
    for i in range(page):
        posts, link = get_posts_list(page_url)
        all_posts += posts
        page_url = urllib.parse.urljoin(INDEX, link)
    return all_posts


def get_articles(metadata):
    post_links = [meta['link'] for meta in metadata]
    with Pool(processes=8) as pool:
        contents = pool.map(fetch_article_content, post_links)
        return contents


def fetch_article_content(link):
    url = urllib.parse.urljoin(INDEX, link)
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    pages = 1

    start = time.time()

    metadata = get_paged_meta(pages)
    articles = get_articles(metadata)

    print('花費: %f 秒' % (time.time() - start))

    print('共%d項結果：' % len(articles))
    for post, content in zip(metadata, articles):
        print('{0} {1: <15} {2}, 網頁內容共 {3} 字'.format(
            post['date'], post['author'], post['title'], len(content)))
