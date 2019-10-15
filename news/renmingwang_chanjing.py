##递归深度超出最大值 '获取单页文本超时'一直超时无法获取文本
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

net_name = '人民网产经'
event_name='事件：盈利亏损'
keyword = '每股盈利'
doc_name = keyword+'.txt'

# data_path='../newsdata/'
data_path='D:\\Projects\\CrawlerLearn\\newsdata'
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5050.400 QQBrowser/10.0.941.400'}

search_url = 'http://industry.people.com.cn/GB/413887/index.html'

def search(keyword,search_url):
    try:
        browser.get(search_url)
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#keyword')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.w1000.clear.logo_line.mt15.o_h > div.fr > form > input[type="image"]:nth-child(5)')))
        input.send_keys(keyword)
        submit.click()
        time.sleep(2)#点击搜索按钮后 待加载出来
        browser.switch_to.window(browser.window_handles[-1])
        page_num = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.w1000.ej_content.mt30 > div > div > div.searchbar_text > b')))
        return page_num.text
    except TimeoutException:
        print('搜索超时')
        return search(keyword,search_url)

def page2():#首页跳转到第二页例外
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.w1000.ej_content.mt30 > div > div > div.page_n > a:nth-child(10)')))
        next_button.click()
    except TimeoutException:
        print('点击下一页超时')
        browser.refresh()

def page6():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.w1000.ej_content.mt30 > div > div > div.page_n > a:nth-child(5)')))
        next_button.click()
    except TimeoutException:
        print('点击下一页超时')
        browser.refresh()

def next_page():
    try:
        next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.w1000.ej_content.mt30 > div > div > div.page_n > a:nth-child(11)')))
        next_button.click()
    except TimeoutException:
        print('点击下一页超时')
        browser.refresh()

def get_one_page_links():#获取单个页面的所有链接
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
    pages =((page_num-1)//20)+1#页面总数
    links_list = get_one_page_links()

    print('第1页，共%d页'%(pages))
    if pages == 1:
        print('1页完')
        return links_list
    print('第2页，共%d页' % (pages))
    time.sleep(2)
    page2()
    links_list = links_list + get_one_page_links()

    for page in range(3, pages+1):
        print('第%d页，共%d页'%(page,pages))
        time.sleep(2)
        next_page()
        links_list = links_list + get_one_page_links()
    print('%d页完'%(pages))
    return links_list


def get_news_text(url):
    try:
        response = requests.get(url,headers=headers)
        response.encoding ='GB2312'
        html = response.text
        try:
            doc = pq(html,parser='html')
            title = doc('.clearfix.w1000_320.text_title h1').text()
            text = doc('.fl.text_con_left .box_con').text()
            whole_text = title+'\n'+text
            return whole_text
        except: 
            pass
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
    for url in enumerate(links_list):
        time.sleep(3)
        text = get_news_text(url)#全文
        text_use=fetch_para(text,keyword)
        if not text is None:
            with open(doc_name,'a',encoding='utf-8') as f1:
                for tu in text_use:
                    f1.write(tu+'\n')

            
def main():
    os.chdir(data_path)
    try:
        os.mkdir(event_name)
    except:
        pass
    os.chdir(data_path+'\\'+event_name)

    page_num = int(search(keyword, search_url))
    if page_num == 0:
        print(keyword + ' 无结果')
    links_list = get_all_links(page_num)#存下所有结果界面的网页链接
    links_num = len(links_list)
    print(net_name+'搜索到的关于 '+keyword+' 的链接数：'+str(links_num))
    if links_num == 0:
        print('无结果')
    print(net_name + ' ' + keyword+' 链接完成')
    get_all_text(keyword, links_list)
    print(net_name + ' ' + keyword+' 文本完成')

if __name__ == '__main__':
    main()