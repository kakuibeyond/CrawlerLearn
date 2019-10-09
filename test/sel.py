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

import os

import requests
from requests.exceptions import RequestException
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10, poll_frequency=1)
links_list = []


def search(keyword,search_url):
    try:
        browser.get(search_url)
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.searchMain > div.searchInput > form > div.search_txt > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.searchMain > div.searchInput > form > div.search_bt > input[type="image"]')))
        input.send_keys(keyword)
        submit.click()
        choose_one()
        get_links()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pagingIndex')))
        return total.text
    except TimeoutException:
        return search()
  
def choose_one():
    try:
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'body > div.searchMain > div.searchbox > div.searchboxCon > div.searchboxL > div > ul > li:nth-child(2) > a')))
        submit.click()
    except TimeoutException:
        print("选择类别超时")
        return choose_one
    
def next_page():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.searchMain > div.searchbox > div.searchboxCon > div.searchboxR > div.pageNav > a.pageNavBtn2')))
        next_button.click()
        get_links()
    except TimeoutException:
        return next_page()

def get_links():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.searchMain > div.searchbox > div.searchboxCon > div.searchboxR > div.searchtext')))
    html = browser.page_source
    doc = pq(html,parser="html")
    items = doc('.searchtext .searchxt a').items()
    for item in items:
        link = item.attr('href')
        links_list.append(link)

def get_news_page(url):
    #wait = WebDriverWait(browser, 10, poll_frequency=2)
    try:
        browser.get(url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.bottom > div.navBottom')))
        return browser.page_source
    except TimeoutException:
        print('timeout')
        return get_news_page(url)
    
def get_news_text(url):
    html = get_news_page(url)
    doc = pq(html)
    title = doc('#the_content #conTit h1').text()
    text = doc('#the_content .textbox #Main_Content_Val').text()
    whole_text = title+'\n'+text
    return whole_text


def get_all_text(keyword):
    os.mkdir(keyword)
    for num,url in enumerate(links_list):
        text = get_news_text(url)
        doc_name = keyword+'\\'+ str(num+1)+'.txt'
        with open(doc_name,'a',encoding='utf-8') as f1:
            f1.write(text)
        
 
def main():
    keyword = '吸收合并'
    search_url = 'http://search.caixin.com/'
    total = search(keyword,search_url)
    return
    current_page,total_pages = total.split('/')
    current_page,total_pages = int(current_page),int(total_pages)
    for i in range(2,min(total_pages+1,5+1)):
        next_page()
    get_all_text(keyword)

if __name__ == '__main__':
    main()
