import requests_html

from ptt import parser


domain = 'https://www.ptt.cc'


class Agent():

    def __init__(self):
        self.session = self._create_session()

    def _create_session(self):
        session = requests_html.HTMLSession(mock_browser=True)
        session.cookies.set('over18', '1')
        return session

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    def get_and_parse(self, url, parser_name):
        resp = self.session.get(url)
        data_parser = getattr(parser, parser_name)
        return data_parser(resp)


agent = Agent()


class Board():

    endpoint = 'index.html'

    def __init__(self, name):
        self.name = name
        self._current_page = None

    def get_meta(self, num: int, after_filename: str = ''):
        self._current_page = None
        if after_filename:
            return self._get_after_filename_meta(num, after_filename)
        else:
            return self._get_newest_meta(num)

    def _get_newest_meta(self, num: int):
        metas = []
        meta_gen = self.get_pagination_meta(pages=None)

        while True:
            batch_meta = list(next(meta_gen))
            metas += batch_meta

            if len(metas) > num:
                metas = metas[:num]
                break

            print(f'Current page: {self._current_page}, '
                  f'number of metas: {len(metas)}')

        return metas

    def _get_after_filename_meta(self, num: int, after_filename: str = ''):
        metas, found = [], False
        meta_gen = self.get_pagination_meta(pages=None)

        while not found:
            batch_meta = list(next(meta_gen))

            for i, meta in enumerate(batch_meta):
                if meta.filename == after_filename:
                    found = True
                    break
            metas += batch_meta[:i]

            print(f'Current page: {self._current_page}, '
                  f'number of metas: {len(metas)}')

        if len(metas) > num:
            metas = metas[-num:]

        return metas

    def get_pagination_meta(self, pages=None):
        viewed_pages = 0
        while True:
            page = self._current_page - 1 if self._current_page else None
            r = agent.get(self.url(page=page))

            meta = parser.post_metas(r)
            self._current_page = parser.current_page_number(r)
            yield reversed(meta)

            viewed_pages += 1
            if pages and viewed_pages >= pages:
                break

    def url(self, page=None):
        page = page if page and isinstance(page, int) else ''
        return f'{domain}/bbs/{self.name}/index{page}.html'

    def search(self,
               title=None,
               thread=None,
               recommend=None,
               author=None,
               num_pages=1):
        url = f'{domain}/bbs/{self.name}/search'

        if title:
            query = title
        elif thread:
            query = f'thread:{thread}'
        elif recommend:
            query = f'recommend:{recommend}'
        elif author:
            query = f'author:{author}'

        params = {'q': query}

        for i in range(num_pages):
            r = agent.get(url, params=params)
            meta = parser.post_metas(r)
            yield meta

            params['page'] = i + 1

    def get_post(self, link):
        url = link if domain in link else f'{domain}{link}'
        r = agent.get(url)
        return parser.post_content(r)


class Ptt():

    def __init__(self, board):
        self.board = Board(board)

    @staticmethod
    def get_post(url):
        r = agent.get(url)
        return parser.post_content(r)
