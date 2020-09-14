# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 11:58:40 2018

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

#==============================================================================
# keywords = ['公开谴责', '责令整改','监管关注函','市场禁入','误导性陈述','重大遗漏',
#             '虚报注册资本','股东虚假出资','超过法定出资期限','票据违法','强制摘牌',
#             '非法集资','信息泄露','占用资金','违规担保','秋后算账','隐瞒关联关系',
#             '禁入']
#==============================================================================
keywords = ['违规担保']
search_url = 'https://www.yicai.com/search?keys='

def search(keyword,search_url):
    try:
        browser.get(search_url)
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#searchkeys2')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.g-doc > div.g-bd.f-cb > div.g-mn.g-mn-w.g-mn-mt1.f-fl > div.m-box5 > div > a')))
        input.send_keys(keyword)
        submit.click()
        time.sleep(3)
        page_num = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#resultcount')))
        return page_num.text
    except TimeoutException:
        print('搜索超时')
        return search(keyword,search_url)

def next_page(page):
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#searchlist > button')))
        print('点击下一页超时')
        next_button.click()
    except TimeoutException:
        return next_page()

def get_one_page_links():
    html = browser.page_source
    doc = pq(html,parser="html")
    items = doc('#searchlist a').items()
    onepage_links_list = []
    for item in items:
        link = item.attr('href')
        onepage_links_list.append('https://www.yicai.com'+link)
    return onepage_links_list

def get_all_links(page_num):
    links_list = []
    if page_num == 0:
        print('无相关结果')
        return
    pages = (page_num-1)//20
    
    pages = min(5,pages+1)
    print('第1页，共%d页'%(pages))
    if pages == 0:
        print('1页完')
        return links_list
    for page in range(2, pages+1):
        print('第%d页，共%d页'%(page,pages))
        time.sleep(3)
        next_page(page)
    time.sleep(3)
    links_list = get_one_page_links()
    print('%d页完'%(pages))
    return links_list


def get_news_text(url):
    try:
        response = requests.get(url,headers=headers)
        html = response.text
        doc = pq(html)
        title = doc('.m-text .title.f-pr').text()
        text = doc('.m-text .m-txt').text()
        whole_text = title+'\n'+text
        return whole_text
    except RequestException:
        print('获取单页文本超时')
        get_news_text(url)

def get_all_text(keyword, links_list):
    for num,url in enumerate(links_list):
        time.sleep(3)
        text = get_news_text(url)
        doc_name = str(num+1)+'.txt'
        with open(doc_name,'a',encoding='utf-8') as f1:
            f1.write(text)
            
def main():
        net_name = '第一财经'
        try:
            os.mkdir('C:\\Users\\ly\\Desktop\\爬虫191212' + '\\' + net_name)
        except:
            pass
        for keyword in keywords:
            os.chdir('C:\\Users\\ly\\Desktop\\爬虫191212' + '\\' + net_name)
            try:
                os.mkdir('C:\\Users\\ly\\Desktop\\爬虫191212' + '\\' + net_name +'\\'+ keyword)
            except:
                pass
            os.chdir('C:\\Users\\ly\\Desktop\\爬虫191212' + '\\' + net_name +'\\'+ keyword)   
            page_num = int(search(keyword, search_url))
            if page_num == 0:
                print(keyword + ' 无结果')
                continue
            links_list = get_all_links(page_num)
            links_num = len(links_list)
            print('链接数：'+str(links_num))
            if links_num == 0:
                print('无结果')
            max_num = min(100,links_num)
            links_list = links_list[0:max_num]
            print(net_name + ' ' + keyword+' 链接完成')
            get_all_text(keyword, links_list)
            print(net_name + ' ' + keyword+' 文本完成')

if __name__ == '__main__':
    main()

