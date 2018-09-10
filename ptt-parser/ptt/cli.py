import json

import click

from ptt import core


@click.command()
@click.option('--board', help='看板名稱')
@click.option('--num', default=50, help='數量')
@click.option('--after_filename', default='', help='文章檔案編號')
@click.option('--filepath', default='', help='存檔位置')
def meta(board, num, after_filename, filepath):
    board = core.Board(board)
    _metas = board.get_meta(num, after_filename)

    filepath = filepath or input('Filepath to save metadata: ')
    assert filepath
    with open(filepath, 'w', encoding='utf8') as f:
        json.dump([
            {field: getattr(m, field, 'None') for field in m.fields}
            for m in _metas
        ], f)


@click.group()
def main():
    pass


main.add_command(meta)


if __name__ == '__main__':
    main()
