# CrawlerTutorial

Python 實際演練：在網路上養了一隻蟲

#安裝相依套件
首先使用 pip 來安裝等會要用的套件，
- requests用來取代內建 urllib 模組，就是比原本的好用！
- lxml用來解析 html/xml，一樣是比原生的有更多優點！
- beautifulsoup 用來分析與抓取html中的元素

```
pip install requests
pip install beautifulsoup
pip install lxml
```

以下就用 PTT 的電影版文章作為我們的爬衝目標囉，嘿嘿！

#第一步：To see is to retrieve，所看即所抓

使用 `requests.get()` 方法來取得網址中的原始碼。
而傳回來的結果是一個包裝起來的物件，真正的純文字原始碼在 `response.text` 中

```python
import requests

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
print(response.text)
```

#第二步：Text interpretation，說說看你看到了什麼？

用 `beautifulsoup` 來解析剛剛抓到的原始碼。
`BeautifulSoup()` 的第二個參數則放入 `lxml` 讓他使用我們剛剛安裝的 lxml 來解析。

而藉由我們自行打開網頁原始碼得知 PTT 網頁版中，
每一篇文章的標題訊息皆放在 `class="r-ent"` 的 `div` 標籤裡。
這裡我們使用到 `find_all()` 方法來指定抓取的目標，尋找之後的結果是一串(`<type: list>`) 文章標題資訊。

```python
import requests
from bs4 import BeautifulSoup

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
articles = soup.find_all('div', 'r-ent')
print(articles)
```

#第三步：所以那標題資訊到底怎麼用？

剛剛說過 `find_all()` 回傳符合的結果，而這串結果是個 `list()` 型態的東西，
所以我們用 `for loop` 來一個一個印出來看看。

而因為 html 本來就是具有階層式的標記語言，
所有的資料都是用 `觀察法` 判斷到底放在哪個標籤、哪一階層裡（觀察系玩家4ni），以下就不多加贅述！

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

    print(title, date, author, link)
```

### 執行結果 (此圖輸出經過特殊處理)
![crawler_3_snap](https://raw.github.com/leVirve/CrawlerTutorial/crawler_3_snap.png)

#第四步：現在 big data 時代捏，都嘛一次要大筆資料！

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
