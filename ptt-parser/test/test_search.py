import ptt


def test_search_recommend():
    board = ptt.Board('movie')
    result = board.search(recommend=20)
    assert result


def test_search_author():
    board = ptt.Board('movie')
    result = board.search(author='hsukai')
    assert result


def test_search_title():
    board = ptt.Board('movie')
    result = board.search(title='哈哈')
    assert result


def test_search_thread():
    board = ptt.Board('movie')
    result = board.search(thread='[ 好雷]  死侍2的各種彩蛋討論')
    assert result


def test_search_pagination():
    board = ptt.Board('movie')
    result_gen = board.search(recommend=20, num_pages=2)
    result = [e for e in result_gen]
    assert len(result) == 2
