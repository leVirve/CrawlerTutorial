import ptt
from ptt.parser import PttParseContentError


def test_get_meta_over18():
    board = ptt.Board('Gossiping')
    meta = board.get_meta(num=20)
    assert len(meta) == 20


def test_get_meta():
    board = ptt.Board('Soft_Job')
    meta = board.get_meta(num=20)
    assert len(meta) == 20

    board = ptt.Board('movie')
    meta = board.get_meta(num=10)
    assert len(meta) == 10

    meta = board.get_meta(num=5, after_filename=meta[-1].filename)
    assert len(meta) == 5


def test_get_pagination_meta():
    board = ptt.Board('Soft_Job')

    paged_meta = board.get_pagination_meta(pages=3)
    meta_list = [meta for meta in paged_meta]

    assert len(meta_list) == 3


def test_get_post_from_meta():
    board = ptt.Board('movie')
    meta = board.get_meta(num=5)

    for m in meta:
        try:
            post = board.get_post(link=m.link)
            break
        except PttParseContentError:
            continue

    assert post
    assert post.ip


def test_get_post_from_url():
    url = 'https://www.ptt.cc/bbs/Soft_Job/M.1467888742.A.259.html'
    post = ptt.Ptt.get_post(url)
    assert post
