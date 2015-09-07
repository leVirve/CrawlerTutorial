# CrawlerTutorial

＜Python 實際演練＞：
在網路上養了一隻蟲，以下就用 PTT 的電影版文章作為我們的爬蟲目標囉！

#相依套件
首先使用 pip 來安裝等會要用的套件，
- requests用來取代內建 urllib 模組，就是比原本的好用！
- beautifulsoup 用來分析與抓取 html 中的元素
- (選用) lxml用來解析 html/xml，一樣是比原生的有更多優點！

```
pip install requests
pip install beautifulsoup
pip install lxml

(if on debain/ubuntu, you may also...)
sudo apt-get install python3-lxml

(if on windows, go find lxml wheel, then...)
pip install lxml‑3.4.4‑cp34‑none‑win32.whl
```

![Unofficial Windows Binaries for lxml](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)

#第一步：所看即所抓 To see is to retrieve

使用 `requests.get()` 函式模擬 HTTP GET 方法來「瀏覽」網頁，並取得網址中的原始碼。
回傳結果是一個 `Beautifulsoup` 包裝起來的物件，而我們真正目標是取得頁面原始碼：真正的純文字原始碼在 `response.text` 中。

```python
import requests

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
print(response.text)
```

#第二步：說說看你看到了什麼？Text Interpretation

用 `Beautifulsoup` 來分析剛剛抓到的原始碼，在 `BeautifulSoup()` 的建構式第二個參數放入 `lxml` 讓他使用我們剛剛安裝的 lxml 來解析。
(p.s. 若剛剛未選擇安裝 `lxml`，則用 Python 內建的 `html.parser` 解析即可。)

而藉由我們打開瀏覽器查看網頁原始碼 (可用`F12` 開發者工具) 得知 PTT 網頁版中，每一篇文章的標題訊息皆放在 `class="r-ent"` 的 `div` 標籤裡。這裡我們使用到 `find_all()` 方法來指定抓取的目標，尋找之後的結果是一串文章列表資訊。

```python
import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')
print(articles)
```

#第三步：所以我說那個標題資訊呢？Hey, here's some meta data

剛剛說過 `find_all()` 回傳符合的結果，而這串結果是個 `list` 型態的東西，所以我們用 `for loop` 來一個一個印出來看看。

而因為 html 本來就是具有階層式的標記語言，所有的資料都是用 `觀察法`判斷到底放在哪個標籤、哪一階層裡（觀察系玩家4ni），以下就不多加贅述！
示範內容抓出：推文數、標題名稱、作者、發文日期和文章網址。

```python
import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')

for article in articles:
    meta = article.find('div', 'title').find('a')

    title = meta.getText().strip()
    link = meta.get('href')
    push = article.find('div', 'nrec').getText()
    date = article.find('div', 'date').getText()
    author = article.find('div', 'author').getText()

    print(push, title, date, author)
```

#### 執行結果 (此圖輸出經過特殊處理)
![crawler_3_snap](https://raw.github.com/leVirve/CrawlerTutorial/master/crawler_3_snap.png)

*特殊處理：* 沒事多寫點程式碼啊！把天賦通通點在美化上吧～

把這段程式碼貼到剛剛的 `crawler_3.py` 裡，並把 `print` 換成 `pretty_print`。漂亮的輸出就出現囉！

``` python
widths = [
        (126,    1), (159,    0), (687,     1), (710,   0), (711,   1),
        (727,    0), (733,    1), (879,     0), (1154,  1), (1161,  0),
        (4347,   1), (4447,   2), (7467,    1), (7521,  0), (8369,  1),
        (8426,   0), (9000,   1), (9002,    2), (11021, 1), (12350, 2),
        (12351,  1), (12438,  2), (12442,   0), (19893, 2), (19967, 1),
        (55203,  2), (63743,  1), (64106,   2), (65039, 1), (65059, 0),
        (65131,  2), (65279,  1), (65376,   2), (65500, 1), (65510, 2),
        (120831, 1), (262141, 2), (1114109, 1),
]


def calc_len(string):
    def chr_width(o):
        global widths
        if o == 0xe or o == 0xf:
            return 0
        for num, wid in widths:
            if o <= num:
                return wid
        return 1
    return sum(chr_width(ord(c)) for c in string)


def pretty_print(push, title, date, author):
    pattern = '%3s\t%s%s%s\t%s'
    padding = ' ' * (50 - calc_len(title))
    print(pattern % (push, title, padding, date, author))

```

#第四步：現在 Big Data 時代捏，給我大數據！

好，那就再開啟 `觀察法` 模式，去找找上一頁的連結在哪裡？
找到了嗎？不是問你頁面上的按鈕在哪裡喔！是看原始碼啊，同學！

相信經過一番搜尋大家都能找的到，
那個按鈕上面有著通往下一步地鑰匙，就是那個連結！抓住他！

```python
import requests
import urllib.parse
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'

NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a


def get_posts(url):
    posts = list()

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', 'r-ent')

    global control
    control = soup.find_all('div', 'pull-right')[0].find_all('a', 'btn')

    for article in articles:
        title_meta = article.find('div', 'title').find('a') or NOT_EXIST
        meta = article.find('div', 'meta')

        post = dict()
        post['link'] = title_meta.get('href', '')
        post['title'] = title_meta.string.strip()
        post['date'] = meta.find('div', 'date').string
        post['author'] = meta.find('div', 'author').string
        posts.append(post)

    return posts

control = None
pages = 5

page_url = url

for i in range(pages):
    posts = get_posts(page_url)
    prev_link = control[1]['href']
    page_url = urllib.parse.urljoin(url, prev_link)
    print(posts)
```

以上就是基本的爬蟲教學課程。
謝謝觀賞～
