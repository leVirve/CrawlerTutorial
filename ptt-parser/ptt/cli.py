import json

from ptt import core


def get_board_meta(
        board_name: str,
        start_aid: str,
        start_date: str
    ):
    board = core.Board(board_name)
    metas = board.get_meta(board_name, start_aid, start_date)
    json.dumps()
