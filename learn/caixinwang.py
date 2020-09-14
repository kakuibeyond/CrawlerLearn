# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 20:27:49 2018

@author: ly
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import requests
import urllib.request

import os
import re

import requests
from requests.exceptions import RequestException
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10, poll_frequency=1)
# done:
keywords = ['战略合作']
search_url = 'http://search.caixin.com/'


def search(keyword,search_url):
    try:
        browser.get(search_url)
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.searchMain > div.searchInput > form > div.search_txt > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.searchMain > div.searchInput > form > div.search_bt > input[type="image"]')))
        input.send_keys(keyword)
        submit.click()
        choose_one()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.searchMain > div.searchkeyword > div > div.keyWordBox01')))
        return total.text
    except TimeoutException:
        print('搜索超时')
        return search()
  
def choose_one():
    try:
        time.sleep(1)
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div.searchMain > div.searchbox > div.searchboxCon > div.searchboxL > div > ul > li:nth-child(2) > a')))
        submit.click()
    except TimeoutException:
        print("选择类别超时")
        return choose_one()
    
def next_page(page):
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.searchMain > div.searchbox > div.searchboxCon > div.searchboxR > div.pageNav > a.pageNavBtn2')))
        next_button.click()
    except TimeoutException:
        print('点击下一页超时')
        return next_page()

#将一页中所有结果的链接存成列表
def get_one_page_links():
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.searchMain > div.searchbox > div.searchboxCon > div.searchboxR > div.searchtext')))
        html = browser.page_source
        doc = pq(html,parser="html")
        items = doc('.searchtext .searchxt a').items()
        onepage_links_list = []
        for item in items:
            link = item.attr('href')
            onepage_links_list.append(link)
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
    pages = min(5,pages+1)
    print('第1页，共%d页'%(pages))
    if pages == 0:
        print('1页完')
        return links_list
    for page in range(2, pages+1):
        print('第%d页，共%d页'%(page,pages))
        time.sleep(2)
        next_page(page)
        links_list = links_list + get_one_page_links()
    print('%d页完'%(pages))
    return links_list
    
#==============================================================================
# def get_links():
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.searchMain > div.searchbox > div.searchboxCon > div.searchboxR > div.searchtext')))
#     html = browser.page_source
#     doc = pq(html,parser="html")
#     items = doc('.searchtext .searchxt a').items()
#     for item in items:
#         link = item.attr('href')
#         links_list.append(link)
# 
#==============================================================================
def get_news_page(url):
    #wait = WebDriverWait(browser, 10, poll_frequency=2)
    try:
        browser.get(url)
        time.sleep(3)
        #等网页更新完成
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.bottom > div.navBottom')))
        return browser.page_source
    except TimeoutException:
        print('获取文本超时')
        print(url)
        time.sleep(10)
        return browser.page_source

def get_news_text(url):
    html = get_news_page(url)
    doc = pq(html)
    title = doc('#the_content #conTit h1').text()
    text = doc('#the_content .textbox #Main_Content_Val').text()
    whole_text = title+'\n'+text
    return whole_text

def get_news_text2(url):#改成request 但会强行关闭连接
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    doc = pq(response.text)
    title = doc('#the_content #conTit h1').text()
    text = doc('#the_content .textbox #Main_Content_Val').text()
    whole_text = title + '\n' + text
    response.close()  # 注意关闭response
    return whole_text

def get_all_text(keyword, links_list):
    for num,url in enumerate(links_list):
        text = get_news_text(url)
        doc_name = str(num+1)+'.txt'
        with open(doc_name,'a',encoding='utf-8') as f1:
            f1.write(text)
        time.sleep(1)  # 自定义
        
 
def main():

    net_name = '财新'
    try:
        os.mkdir('D:\\学习\\爬虫' + '\\' + net_name)
    except:
        pass
    for keyword in keywords:
        os.chdir('D:\\学习\\爬虫' + '\\' + net_name)
        try:
            os.mkdir('D:\\学习\\爬虫' + '\\' + net_name +'\\'+ keyword)
        except:
            pass
        os.chdir('D:\\学习\\爬虫' + '\\' + net_name +'\\'+ keyword)
        result = search(keyword, search_url)
        res =  re.findall('大约 (\d+) 条查询结果', result)
        if len(res) == 0:
            print(keyword + ' 无结果')
            continue
        page_num = int(res[0])
        links_list = get_all_links(page_num)
        links_num = len(links_list)
        print('链接数：'+str(links_num))
        if links_num == 0:
            print('无结果')
        max_num = min(100,links_num)
        links_list = links_list[0:max_num]
        print(net_name + ' ' + keyword+' 链接完成')
        # print(links_list)
        get_all_text(keyword, links_list)
        print(net_name + ' ' + keyword+' 文本完成')

if __name__ == '__main__':
    main()