import ptt


def demo():
    spider = Spider('Soft_Job')
    url = 'https://www.ptt.cc/bbs/movie/M.1497069176.A.600.html'
    url = 'https://www.ptt.cc/bbs/Soft_Job/M.1467888742.A.259.html'
    print(spider.get_total_page_num())


def main():
    ptt_board = ptt.Board('Gossiping')
    resp = ptt_board.get_meta(num=5)
    for i, m in enumerate(resp):
        print(i, m.title, m.link)
        if '公告' in m.title:
            continue
        r = ptt_board.post(link=m.link)
        print(r.content)


if __name__ == '__main__':
    main()
