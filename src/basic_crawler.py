import re
import time
import urllib
from multiprocessing import Pool

import rich
import rich.table
from requests_html import HTMLSession


# 解析文章列表中的元素
def parse_article_entries(elements):
    results = []
    for element in elements:
        try:
            push = element.find('.nrec', first=True).text
            mark = element.find('.mark', first=True).text
            title = element.find('.title', first=True).text
            author = element.find('.meta > .author', first=True).text
            date = element.find('.meta > .date', first=True).text
            link = element.find('.title > a', first=True).attrs['href']
        except AttributeError:
            # 處理文章被刪除的情況
            if '(本文已被刪除)' in title:
                match_author = re.search('\[(\w*)\]', title)
                if match_author:
                    author = match_author.group(1)
            elif re.search('已被\w*刪除', title):
                match_author = re.search('\<(\w*)\>', title)
                if match_author:
                    author = match_author.group(1)
        # 將解析結果加到回傳的列表中
        results.append({
            'push': push,
            'mark': mark,
            'title': title,
            'author': author,
            'date': date,
            'link': link
        })
    return results


# 解析「上頁」的連結
def parse_next_link(controls):
    link = controls[1].attrs['href']
    return urllib.parse.urljoin('https://www.ptt.cc/', link)


def get_posts(post_links):
    with Pool(processes=8) as pool:
        responses = pool.map(session.get, post_links)
        return responses


def main():
    url = 'https://www.ptt.cc/bbs/movie/index.html'

    num_page = 3
    post_links = []
    for page in range(num_page):
        response = session.get(url)
        # 解析文章列表的元素
        metadata = parse_article_entries(elements=response.html.find('div.r-ent'))
        # 解析下一頁的連結
        next_page_url = parse_next_link(controls=response.html.find('.action-bar a.btn.wide'))
        # 一串文章的 URL
        post_links += [urllib.parse.urljoin(url, meta['link']) for meta in metadata]

        table = rich.table.Table(show_header=False, width=120, title=f'{page=}')
        for result in metadata:
            table.add_row(*list(result.values()))
        rich.print(table)

        url = next_page_url

    start_time = time.time()
    results = get_posts(post_links)
    print(f'花費: {time.time() - start_time:.6f}秒，共 {len(results)} 篇文章')


if __name__ == '__main__':
    session = HTMLSession()
    session.cookies.set('over18', '1')
    main()
