# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 20:24:09 2018

@author: ly
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 16:44:10 2018

@author: ly
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 21:48:17 2018

@author: ly
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq

import re
import os

import requests
from requests.exceptions import RequestException
import time

page_lists = []
keyword = '战略合作'
url_left = 'http://news.toocle.com/search/index.php?_d=news&_a=news_search&f=search&terms=%E6%88%98%E7%95%A5%E5%90%88%E4%BD%9C&p='

for i in range(45,50):
    pre_page = url_left + str(i+1)
    page_lists.append(pre_page)

def get_one_page_links(url):

    try:
        req = requests.get(url)
        html = req.text
        doc = pq(html,parser="html")
        items = doc('.content .left2 .zixun_list a').items()
        onepage_links_list = []
        for item in items:
            onepage_links_list.append('http://news.toocle.com'+item.attr('href'))
        return onepage_links_list
    except TimeoutException:
        print('获取单个页面链接超时')
        return get_one_page_links()

def get_all_links():
    links_list = []
    for page in page_lists:
        links_list = links_list + get_one_page_links(page)

    return links_list

def get_news_text(url):
    try:
        response = requests.get(url)
        html = response.text
        try:
            doc = pq(html,parser='html')
            title = doc('.content .content_right .text').text()
            text = doc('.content .content_right .print4').text()
            whole_text = title+'\n'+text
            return whole_text
        except:
            pass
    except RequestException:
        print('获取单页文本超时')
        get_news_text(url)


def get_all_text(keyword, links_list):
    for num,url in enumerate(links_list):
        time.sleep(3)
        text = get_news_text(url)
        doc_name = str(num+451) + '.txt'
        if not text is None:
            with open(doc_name, 'a', encoding='utf-8') as f1:
                f1.write(text)


def main():
    net_name = '生意'
    try:
        os.mkdir('D:\\学习\\爬虫' + '\\' + net_name)
    except:
        pass

    os.chdir('D:\\学习\\爬虫' + '\\' + net_name)
    try:
        os.mkdir('D:\\学习\\爬虫' + '\\' + net_name +'\\'+ keyword)
    except:
        pass

    os.chdir('D:\\学习\\爬虫' + '\\' + net_name +'\\'+ keyword)

    links_list = get_all_links()
    get_all_text(keyword, links_list)

if __name__ == '__main__':
    main()