import os
import re

from lxml import etree
from pyquery import PyQuery
from requests_html import HTMLResponse

from ptt.model import PostMeta, Post, Push


def current_page_number(r: HTMLResponse):
    xpath = '//*[@id="action-bar-container"]/div/div[2]/a[2]'
    prev_url = xpath_attr(r.html, xpath, attr='href')

    match = re.search(r'index(\d+)', prev_url)
    current_page_number = int(match.group(1)) + 1 if match else 0

    return current_page_number


def post_metas(r: HTMLResponse):
    entries = r.html.find('div.r-ent')

    parsing_rule = dict(
        push='.nrec',
        mark='.mark',
        title='.title',
        date='.meta > .date',
        author='.meta > .author',
        link='.title > a'
    )

    def parse_entry(ent):
        e = {}
        for field, selector in parsing_rule.items():
            try:
                e[field] = selected_text(ent, selector)
                if field == 'link':
                    e[field] = selected_attr(ent, selector, 'href')
                    e['filename'], _ = os.path.splitext(
                        os.path.basename(e['link']))
            except Exception as err:
                print(err)
        return e

    return [PostMeta(**parse_entry(ent)) for ent in entries]


def post_content(r: HTMLResponse):

    def parse_metaline():
        metaline = main.find('div.article-metaline')

        author = metaline[0].find('span')[1].text
        title = metaline[1].find('span')[1].text
        datetime = metaline[2].find('span')[1].text
        return author, title, datetime

    def parse_postline():
        ip_text = main.find(
            'span', containing='發信站: 批踢踢實業坊(ptt.cc)', first=True).text
        # sometimes fails due to span+a (default: span>a)
        url = main.find(
            'span', containing='文章網址:', first=True).find(
                'a', first=True).attrs.get('href')

        match = re.search(r'\d+\.\d+\.\d+\.\d+', ip_text)
        ip = match[0] if match else ''

        return ip, url

    def parse_comments():

        def get_comment():
            for push in main.find('div.push'):
                yield push.find('span')

        return [
            Push(
                push=spans[0].text.strip(),
                author=spans[1].text.strip(),
                comment=spans[2].text[1:].strip(),
                datetime=spans[3].text.strip()
            ) for spans in get_comment()]

    def parse_content():
        exclude_classes = [
            '.article-metaline', '.article-metaline-right', '.push']
        exclude_text_spans = ['發信站: 批踢踢實業坊(ptt.cc)', '文章網址:']

        for exclude_text in exclude_text_spans:
            ele = main.lxml.xpath(
                f'//span[contains(text(),"{exclude_text}")]')[0]
            ele.getparent().remove(ele)
        cleaned_html = etree.tostring(main.lxml, encoding='UTF-8')


        cleaned_pq = PyQuery(cleaned_html)
        for exclude_cls in exclude_classes:
            cleaned_pq.remove(exclude_cls)

        return cleaned_pq.text(squash_space=False)

    try:
        main = r.html.find('#main-content', first=True)

        author, title, datetime = parse_metaline()
        ip, url = parse_postline()

        return Post(
            author=author, title=title, ip=ip, url=url,
            full_datetime=datetime,
            comments=parse_comments(),
            content=parse_content())
    except IndexError:
        raise PttParseContentError


class PttParseContentError(Exception):
    pass


''' General Utils '''


def selected_text(ent, sel):
    return ent.find(sel, first=True).text


def selected_attr(ent, sel, attr):
    return ent.find(sel, first=True).attrs.get(attr)


def xpath_attr(ent, sel, attr):
    return ent.xpath(sel, first=True).attrs.get(attr)
