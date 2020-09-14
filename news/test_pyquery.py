
from pyquery import PyQuery as pq
import requests

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5050.400 QQBrowser/10.0.941.400'}
url='http://www.nbd.com.cn/articles/2010-10-16/395470.html'
response = requests.get(url,headers=headers)
html = response.text
doc=pq(html)

title = doc('.g-main .g-article-left .g-article .g-article-top h1').text()
        # /html/body/div[4]/div[1]/div[2]/div[1]/h1/text()
        # body > div.g-main > div.g-article-left > div.g-article > div.g-article-top > h1
        #   糖价企稳促扩张 南宁糖业拟收购远丰糖业75%股权
        # /html/body/div[4]/div[1]/div[2]/div[1]/h1/text()
text = doc('.g-main .g-article .g-articl-text').text()
whole_text = title+'\n'+text

print(title)

