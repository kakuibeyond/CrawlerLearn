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


import os

import requests
from requests.exceptions import RequestException
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10, poll_frequency=1)

keyword = '吸收合并'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5050.400 QQBrowser/10.0.941.400'}

search_url = 'http://industry.people.com.cn/GB/413887/index.html'

def search(keyword,search_url):
    try:
        browser.get(search_url)
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#keyword')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.w1000.clear.logo_line.mt15.o_h > div.fr > form > input[type="image"]:nth-child(5)')))
        input.send_keys(keyword)
        submit.click()
        time.sleep(2)
        browser.switch_to.window(browser.window_handles[1])
        page_num = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.w1000.ej_content.mt30 > div > div > div.searchbar_text > b')))
        return page_num.text
    except TimeoutException:
        print('搜索超时')
        return search(keyword,search_url)

def next_page():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.main > div.main-left > div.pagination > span.next > a')))
        next_button.click()
    except TimeoutException:
        print('点击下一页超时')
        browser.refresh()

def get_one_page_links():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.w1000.ej_content.mt30 > div > div > div.page2_list')))
        html = browser.page_source
        doc = pq(html,parser="html")
        items = doc('.page2_list h2 a').items()
        onepage_links_list = []
        for item in items:
            onepage_links_list.append(item.attr('href'))
        return onepage_links_list
    except TimeoutException:
        print('获取单个页面链接超时')
        return get_one_page_links()

def get_all_links(page_num):
    links_list = []
    if page_num == 0:
        print('无相关结果')
        return
    pages = (page_num-1)//20
    links_list = get_one_page_links()
    print('第1页，共%d页'%(pages+1))
    if pages == 0:
        print('1页完')
        return links_list
    for page in range(1, min(5,pages)+1):
        print('第%d页，共%d页'%(page,pages+1))
        time.sleep(1)
        next_page()
        links_list = links_list + get_one_page_links()
    print('%d页完'%(pages+1))
    return links_list


def get_news_text(url):
    try:
        response = requests.get(url,headers=headers)
        response.encoding ='GB2312'
        html = response.text
        doc = pq(html,parser='html')
        title = doc('.clearfix.w1000_320.text_title h1').text()
        text = doc('.fl.text_con_left .box_con').text()
        whole_text = title+'\n'+text
        return whole_text
    except RequestException:
        print('获取单页文本超时')
        get_news_text(url)


def get_all_text(keyword, links_list):
    keyword = keyword+'-人民网产经'
    os.mkdir(keyword)
    for num,url in enumerate(links_list):
        time.sleep(3)
        text = get_news_text(url)
        doc_name = keyword+'\\'+ str(num+1)+'.txt'
        with open(doc_name,'a',encoding='utf-8') as f1:
            f1.write(text)

page_num = int(search(keyword, search_url))
links_list = get_all_links(page_num)
links_num = len(links_list)
if links_num == 0:
    print('无结果')
max_num = min(100,links_num)
links_list = links_list[0:max_num]
print('人民网产经 '+keyword+' 链接完成')
browser.close()
get_all_text(keyword, links_list)
print('人民网产经 '+keyword+' 文本完成')

