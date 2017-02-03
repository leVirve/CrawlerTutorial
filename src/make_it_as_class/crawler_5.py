import re
import requests
import urllib.parse
from bs4 import BeautifulSoup


class PTTCrawler():

    url = 'https://www.ptt.cc/bbs/movie/index.html'
    NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

    def __init__(self):
        self.posts = list()
        self.ctrl = None
        self.next_url = PTTCrawler.url
        self.total_pages = 0

    def get_recent_page(self, pages):
        for i in range(pages):
            if i == 1:
                self.count_pages()
            self.get_posts_list(self.next_url)
            self.next_url = self.get_next_url()
        return self.posts

    def get_next_url(self):
        prev_link = self.ctrl[1]['href']
        return urllib.parse.urljoin(PTTCrawler.url, prev_link)

    def count_pages(self):
        prev_page_counter = re.findall('index(\d+?).html', self.next_url)
        self.total_pages = int(prev_page_counter[0]) + 1

    def get_posts_list(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        articles = soup.find_all('div', 'r-ent')

        self.ctrl = soup.find('div', 'btn-group-paging').find_all('a', 'btn')

        for article in articles:
            title_meta = article.find('div', 'title').find('a') \
                or PTTCrawler.NOT_EXIST
            meta = article.find('div', 'meta')

            post = dict()
            post['link'] = title_meta.get('href', '')
            post['title'] = title_meta.string.strip()
            post['date'] = meta.find('div', 'date').string
            post['author'] = meta.find('div', 'author').string
            self.posts.append(post)

if __name__ == '__main__':
    ptt = PTTCrawler()
    results = ptt.get_recent_page(3)

    print(results)
