import ptt


def enumerate_meta():
    ptt_board = ptt.Board('Soft_Job')
    resp = ptt_board.get_meta(num=5)
    for i, m in enumerate(resp):
        if '公告' in m.title:
            continue
        r = ptt_board.get_post(link=m.link)
        print(i, m.title, m.link, f', words: {len(r.content)}')


def main():
    board = ptt.Board('movie')

    meta = board.get_meta(num=10)
    meta = board.get_meta(num=5, after_filename=meta[-1].filename)
    assert len(meta) == 5

    for m in meta:
        print(f'推文數: {m.push} ',
              f'標記: {m.mark} ',
              f'標題: {m.title} ',
              f'日期: {m.date} ',
              f'作者: {m.author} ',
              f'連結: {m.link} ',
              f'文章檔案編號: {m.filename} ',
              )



if __name__ == '__main__':
    enumerate_meta()
    main()
