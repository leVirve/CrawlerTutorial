# CrawlerTutorial

＜Python 實際演練＞：
在網路上養了一隻蟲，以下就用 PTT 的電影版文章作為我們的爬蟲目標囉！

#相依套件
首先使用 pip 來安裝等會要用的套件，
- requests 用來取代內建 urllib 模組，就是比原本的好用！
- beautifulsoup 用來分析與抓取 html 中的元素
- (選用) lxml 用來解析 html/xml，一樣是比原生的有更多優點！

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
相信都有發現了，關於頁面跳轉的超連結就放在 `<div class='pull-right'>` 的 `<a class='btn'>` 裡，所以我們可以像這樣抓到他們：

```python
# 控制頁面選項: 最舊/上頁/下頁/最新
control = soup.find('div', 'pull-right').find_all('a', 'btn')
```

而我們需要的是`上一頁`的功能，為什麼呢？因為 PTT 是最新的文章顯示在前面啊～所以要挖資料必須往前翻。

那怎麼使用呢？先去抓出 `control` 中第二個(index: [1])的 `href`，然後他可能長這樣 `/bbs/movie/index3237.html`；而完整的網址(URL)必須要有 `https://www.ptt.cc/` 開頭，所以用 `urljoin()` 把 Movie 首頁連結和新的 link 比對合併成完整的 URL！

```python
prev_link = control[1].get('href')
page_url = urllib.parse.urljoin(INDEX, prev_link)
```


另外，或許會發現怎麼前面的程式有時候會出錯啊？！看看網頁版發現原來當該頁面中有文章被刪除時，網頁上的 `＜本文已被刪除＞` 這個元素的原始碼 `結構` 和原本不一樣哇！所以我們用 `BeautifulSoup` 生一個 `<a>` 元素來替代，方便後面存取時使用 (避免 title 和 link 的地方對 `None` 存取，產生上述提到的錯誤)。

```python

NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

...

# meta = A or B，當前面 A 的 .find() 抓到的是空的，則讓 meta 等於 B
meta = article.find('div', 'title').find('a') or NOT_EXIST
```

現在我們將函式重新定義，讓：
- `get_posts_on_page(url)`:
抓取一頁中所有的文章的 metadata (很潮的`後設資料`)，並回傳一串 `key-value` 類型的資料。
- `get_pages(num)`:
抓取最新的 N 個頁面，並指派 `get_posts_on_page` 去抓每頁面中的資料，把每一串資料合併成一大串後回傳。

```python
# 每筆資料長這樣子，dict() 類型資料：key-value pairs data
{
    'title': meta.getText().strip(),
    'link': meta.get('href'),
    'push': article.find('div', 'nrec').getText(),
    'date': article.find('div', 'date').getText(),
    'author': article.find('div', 'author').getText(),
}
```

而 `get_posts_on_page(url)` 和 `get_pages(num)` 回傳的就是這樣的一串資料：
```python
[
{'date': ' 9/07', 'author': 'zkow', 'title': 'Fw: [新聞] 小貝進好萊塢拍電影啦！', 'push': '', 'link': '/bbs/movie/M.1441633014.A.B4F.html'},
{'date': ' 9/07', 'author': 'catlover7', 'title': '關於我的少女時代小疑問', 'push': '2', 'link': '/bbs/movie/M.1441633103.A.735.html'},
{'date': ' 9/07', 'author': 'cake10414', 'title': '[贈序號] 贈Ez訂app電影68折優待序號(已發出)', 'push': '', 'link': '/bbs/movie/M.1441633338.A.235.html'},
{'author': 'soulx', 'date': ' 9/07', 'push': '4', 'title': '[新聞] 侯孝賢：「一個導演，沒有自覺，就不用玩', 'link': '/bbs/movie/M.1441633354.A.961.html'},
{'author': 'Takuri', 'date': ' 9/07', 'push': '', 'title': '[請益] 倖存者（The Remaining)的結局', 'link': '/bbs/movie/M.1441636396.A.D64.html'},
...
]
```


附上**crawler_4.py 完整程式碼**

另外要說明的是 `from utils import pretty_print`，把剛剛 **crawler_3.py** 那個漂亮的輸出功能數十行的程式碼放到同目錄底下的新檔案 `utils.py` 中(檔案名字你喜歡就好，只要記得 `from xxx import pretty_print` 要記得一起改)，然後在這邊 `import`(相當於 C語言中的 include )就能繼續沿用功能！

```python
import requests
import urllib.parse
from bs4 import BeautifulSoup

from utils import pretty_print

url = 'https://www.ptt.cc/bbs/movie/index.html'
NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

control = None


def get_posts_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    global control
    control = soup.find('div', 'pull-right').find_all('a', 'btn')
    articles = soup.find_all('div', 'r-ent')

    posts = list()
    for article in articles:
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        posts.append({
            'title': meta.getText().strip(),
            'link': meta.get('href'),
            'push': article.find('div', 'nrec').getText(),
            'date': article.find('div', 'date').getText(),
            'author': article.find('div', 'author').getText(),
        })
    return posts


def get_pages(num):
    page_url = index_url
    all_posts = list()
    for i in range(num):
        all_posts += get_posts_on_page(page_url)
        prev_link = control[1].get('href')
        page_url = urllib.parse.urljoin(index_url, prev_link)
    return all_posts


for post in get_pages(2):
    pretty_print(post['push'], post['title'], post['date'], post['author'])
```

**上面的程式碼都在 `src/` 中可以找到！**

以上就是基本的爬蟲入門教學～還望各位看官喜歡

謝謝觀賞～
