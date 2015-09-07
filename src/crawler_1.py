import requests

url = 'https://www.ptt.cc/bbs/movie/index.html'
response = requests.get(url)
print(response.text)
