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

        # get the posts content
        self.get_articles()

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

    def get_articles(self):
        for post in self.posts:
            url = urllib.parse.urljoin(PTTCrawler.url, post['link'])
            response = requests.get(url)
            post['content'] = response.text


if __name__ == '__main__':
    ptt = PTTCrawler()

    import time
    start = time.time()
    posts = ptt.get_recent_page(5)
    print('花費: %f 秒' % (time.time() - start))

    print('共%d項結果：' % len(posts))
    for post in posts:
        print('{0} {1: <15} {2}'.format(
            post['date'], post['author'], post['title']))
