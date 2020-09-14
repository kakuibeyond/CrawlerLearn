# -*- coding:gbk -*-
from bs4 import BeautifulSoup
import requests

url = 'http://www.baidu.com/s?rtt=1&bsst=1&cl=2&tn=news&word=%E6%88%98%E7%95%A5%E5%90%88%E4%BD%9C'
req = requests.get(url)
soup = BeautifulSoup(req.text,'html.parser')
news_lists = soup.find_all('div','result')
print(len(news_lists))
for news in news_lists:
    h3 = news.select('h3')
    author = news.select('p')
    print(h3,author)