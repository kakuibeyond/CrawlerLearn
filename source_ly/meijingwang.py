# -*- coding: utf-8 -*-
# 需要点击'加载更多'不断在一个网页上面查看（url没有变化）
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

browser = webdriver.Chrome()#打开浏览器
wait = WebDriverWait(browser, 10, poll_frequency=1)

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5050.400 QQBrowser/10.0.941.400'}
net_name = '每经网'
event_name='事件：盈利亏损'
keywords = ['每股盈利']
data_path=r'D:\Projects\CrawlerLearn\newsdata'
search_url = 'http://www.nbd.com.cn/'

def search(keyword,search_url):
    try:
        browser.get(search_url)#进入网页
        #等到搜索框出现
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        #等到搜索按钮可以点击
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.g-top > div > div > form > input.u-magnifier')))
        input.send_keys(keyword)
        submit.click()
        time.sleep(1)
        page_num = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.main > div.main-left > div.search > h1 > span')))
        return page_num.text#body > div.search-column1 > div.right-content > a对应'加载更多’按钮
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

#根据关键词选出有用的段落 标题也视为一个段落
def fetch_para(text,keyword):
    text_list=text.splitlines()
    #返回字符串列表， 不过分隔符为(’\r’, ‘\r\n’, \n’)，也就是说按照行分隔
    useful_para=[]
    for e in text_list:
        if keyword in e:
            useful_para.append(e)
    return useful_para

def get_all_text(keyword, links_list):
    for url in links_list:
        text = get_news_text(url)
        text_use=fetch_para(text,keyword)
        if not text is None:
            with open(keyword+'.txt','a',encoding='utf-8') as f1:
                for tu in text_use:
                    f1.write(tu+'\n')
        time.sleep(1)  # 自定义
            
def main():
    os.chdir(data_path)
    try:
        os.mkdir(net_name)
    except:
        pass
    os.chdir(data_path+'\\'+net_name)
    try:
        os.mkdir(event_name)
    except:
        pass
    os.chdir(data_path+'\\'+net_name+'\\'+event_name)
    for keyword in keywords:
        with open(keyword+'.txt','a') as f0:
            pass

        page_num = int(search(keyword, search_url).split(' ')[1])
        links_list = get_all_links(page_num)
        links_num = len(links_list)
        if links_num == 0:
            print('无结果')
        max_num = min(20,links_num)
        links_list = links_list[0:max_num]
        print('每经网 '+keyword+' 链接完成')
        get_all_text(keyword, links_list)
        print('每经网 '+keyword+' 文本完成')

if __name__ == '__main__':
    main()