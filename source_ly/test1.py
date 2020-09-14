# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 21:37:51 2018

@author: ly
"""
import urllib.request
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlencode
urlleft = 'http://search.caixin.com/search/search.jsp?keyword='
urlright = 'x=42&y=14&channel=0&time=&type=1&sort=1&startDate=&endDate=&special=false'
targetword = '吸收合并'
targetword = urllib.request.quote(targetword)
url = urlleft+targetword+urlright
#response = urllib.request.urlopen(url)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
res = requests.get(url, headers=headers)
with open('caixin.txt','a') as f1:
    f1.write(res.text)
soup = BeautifulSoup(res.text,'lxml')
