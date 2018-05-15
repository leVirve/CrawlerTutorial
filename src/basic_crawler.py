import re
import time
import urllib
from multiprocessing import Pool

import requests
from requests_html import HTML

from utils import pretty_print  # noqa


def fetch(url):
    ''' Step-1: send a request and fetch the web page.
    '''
    response = requests.get(url)
    return response


def parse_article_entries(doc):
    ''' Step-2: parse the post entries on the source string.
    '''
    html = HTML(html=doc)
    post_entries = html.find('div.r-ent')
    return post_entries


def parse_article_meta(ent):
    ''' Step-3: parse the metadata in article entry
    '''
    meta = {
        'title': ent.find('div.title', first=True).text,
        'push': ent.find('div.nrec', first=True).text,
        'date': ent.find('div.date', first=True).text,
    }

    try:
        meta['author'] = ent.find('div.author', first=True).text
        meta['link'] = ent.find('div.title > a', first=True).attrs['href']
    except AttributeError:
        if '(本文已被刪除)' in meta['title']:
            match_author = re.search('\[(\w*)\]', meta['title'])
            if match_author:
                meta['author'] = match_author.group(1)
        elif re.search('已被\w*刪除', meta['title']):
            match_author = re.search('\<(\w*)\>', meta['title'])
            if match_author:
                meta['author'] = match_author.group(1)
    return meta


def get_metadata_from(url):
    ''' Step-4: parse the link of previous link.
    '''

    def parse_next_link(doc):
        ''' Step-4a: parse the link of previous link.
        '''
        html = HTML(html=doc)
        controls = html.find('.action-bar a.btn.wide')
        link = controls[1].attrs.get('href')
        return urllib.parse.urljoin(domain, link)

    resp = fetch(url)
    post_entries = parse_article_entries(resp.text)
    next_link = parse_next_link(resp.text)

    metadata = [parse_article_meta(entry) for entry in post_entries]
    return metadata, next_link


def get_paged_meta(url, num_pages):
    ''' Step-4-ext: collect pages of metadata starting from url.
    '''
    collected_meta = []

    for _ in range(num_pages):
        posts, link = get_metadata_from(url)
        collected_meta += posts
        url = urllib.parse.urljoin(domain, link)

    return collected_meta


def partA():
    resp = fetch(start_url)
    post_entries = parse_article_entries(resp.text)
    for entry in post_entries:
        meta = parse_article_meta(entry)
        pretty_print(meta['push'], meta['title'], meta['date'], meta['author'])


def partB():
    metadata = get_paged_meta(start_url, num_pages=5)
    for meta in metadata:
        pretty_print(meta['push'], meta['title'], meta['date'], meta['author'])


def partC():

    def get_posts(metadata):
        post_links = [
            urllib.parse.urljoin(domain, meta['link'])
            for meta in metadata if 'link' in meta]

        with Pool(processes=8) as pool:
            contents = pool.map(fetch, post_links)
            return contents

    start = time.time()

    metadata = get_paged_meta(start_url, num_pages=2)
    resps = get_posts(metadata)

    print('花費: %f 秒' % (time.time() - start))

    print('共%d項結果：' % len(resps))
    for post, resps in zip(metadata, resps):
        print('{0} {1: <15} {2}, 網頁內容共 {3} 字'.format(
            post['date'], post['author'], post['title'], len(resps.text)))


domain = 'https://www.ptt.cc/'
start_url = 'https://www.ptt.cc/bbs/movie/index.html'


if __name__ == '__main__':
    partA()
    partB()
    partC()
