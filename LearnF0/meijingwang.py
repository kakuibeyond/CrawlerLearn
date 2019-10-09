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
#done:'公开谴责', '责令整改','监管关注函','市场禁入','误导性陈述','重大遗漏','虚报注册资本','股东虚假出资','超过法定出资期限','票据违法','强制摘牌','非法集资','信息泄露','占用资金','违规担保','秋后算账','隐瞒关联关系','禁入'
keywords = ['战略合作']

search_url = 'http://www.nbd.com.cn/'

def search(keyword,search_url):
    try:
        browser.get(search_url)
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.g-top > div > div > form > input.u-magnifier')))
        input.send_keys(keyword)
        submit.click()
        time.sleep(1)

        submit2 = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.search-column1 > div.left-suffix > div > ul.label-block.js-result > li:nth-child(2)')))
        submit2.click()
        page_num = wait.until(EC.presence_of_element_located((By.xpath,'/html/body/div[4]/div[2]/div/p/text()[2]')))
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
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.main > div.main-left > ul')))
        html = browser.page_source
        doc = pq(html,parser="html")
        items = doc('.main .search-text.mt15 .articleMaterial_title a').items()
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
    pages = (page_num-1)//15
    links_list = get_one_page_links()
    pages = min(7,pages+1)
    print('第1页，共%d页'%(pages))
    if pages == 0:
        print('1页完')
        return links_list
    for page in range(2,  pages+1):
        print('第%d页，共%d页'%(page,pages))
        time.sleep(2)
        next_page()
        links_list = links_list + get_one_page_links()
    print('%d页完'%(pages))
    return links_list


def get_news_text(url):
    try:
        response = requests.get(url,headers=headers)
        html = response.text
        doc = pq(html)
        title = doc('.g-main .g-article .g-article-top h1').text()
        text = doc('.g-main .g-article .g-articl-text').text()
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
    net_name = '每经网'
    try:
        os.mkdir('D:\\学习\\爬虫' + '\\' + net_name)
    except:
        pass
    for keyword in keywords:
        os.chdir('D:\\学习\\爬虫' + '\\' + net_name)
        try:
            os.mkdir('D:\\学习\\爬虫' + '\\' + net_name + '\\' + keyword)
        except:
            pass
        os.chdir('D:\\学习\\爬虫' + '\\' + net_name + '\\' + keyword)

        links_list = get_all_links(page_num)
        links_num = len(links_list)
        if links_num == 0:
            print('无结果')
        max_num = min(100,links_num)
        links_list = links_list[0:max_num]
        print('每经网 '+keyword+' 链接完成')
        get_all_text(keyword, links_list)
        print('每经网 '+keyword+' 文本完成')

if __name__ == '__main__':
    main()