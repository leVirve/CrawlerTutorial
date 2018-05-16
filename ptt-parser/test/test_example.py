import json

import ptt


def test_save_meta():
    board = ptt.Board('movie')
    meta = board.get_meta(num=10)

    s = json.dumps(meta)
    assert s


def test_save_search_result():
    board = ptt.Board('movie')
    result = board.search(recommend=20)

    s = json.dumps(result)
    assert s
