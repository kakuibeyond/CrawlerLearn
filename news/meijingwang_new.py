# -*- coding: utf-8 -*-
#存好结果界面的url列表 然后再放到服务器上面用requests+pyquery爬取
# keyword匹配段落 只存匹配到的段落（或标题
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
event_name='事件：收购重组'
keywords = ['股权收购']
#事件：盈利亏损5634 ['亏转盈','盈转亏','每股盈利','扭亏为盈','营收增长','利润上升','利润下降']
#事件：报告公告10761 ['公开转让','财务报表','季度报告','年度报告','临时议案','业绩快报','澄清公告']
#事件：收购重组2485 ['放弃收购','资产置换','要约收购','股权收购']
#事件：上市退市10950 ['挂牌上市','公开挂牌','终止上市','恢复上市','暂停上市','IPO上市','买壳上市']
#事件：高管变动907 ['高管辞职','高管变动','高管任职']
#事件：违法纠纷7313 ['合同纠纷','股权纠纷','借款纠纷','公开谴责','通报批评','监管工作函','重大遗漏','强制摘牌','非法集资'
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
        page_num = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.search-column1 > div.right-content > div > p')))
        return page_num.text#您搜索每股盈利获得大约 642 条查询结果(搜索用时0.013)
    except TimeoutException:
        print('搜索超时')
        return search(keyword,search_url)


def get_all_links():
    print('正在加载所有结果列表……')
    j=0
    while(True):
        try:
            more_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.search-column1 > div.right-content > a')))
            more_button.click()
            j=j+1
            time.sleep(1)
            if(j>=249):#限定链接数最多为2000条 最多点击249次
                break
        except TimeoutException:
            print('加载全部完成')
            break
    
    html = browser.page_source#网页源码
    doc = pq(html,parser="html")#解析网页
    items = doc('.search-list li a').items()
    links_list = []
    for item in items:
        links_list.append(item.attr('href'))
    print('所有链接url获取完成')
    return links_list

def get_news_text(url):
    try:
        response = requests.get(url,headers=headers)
        html = response.text
        doc = pq(html)
        title = doc('.g-main .g-article-left g-article .g-article-top h1').text()
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
    print('正在获取文本信息')
    i=1
    for url in links_list:
        if((i-1)%50==0):
            print('正在处理第%d-%d条信息'%(i,i+50))
        text = get_news_text(url)
        text_use=fetch_para(text,keyword)
        if not text is None:
            with open(keyword+'.txt','a',encoding='utf-8') as f1:
                for tu in text_use:
                    f1.write(tu+'\n')
        i=i+1
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

        links_num=search(keyword, search_url).split()[1]
        print(net_name+'搜索到关于 '+keyword+' 的新闻有： '+links_num+' 条。')
        links_list = get_all_links()
        links_num = len(links_list)
        if links_num == 0:
            print('无结果')
        # max_num = min(30,links_num)
        # links_list = links_list[0:max_num]
        get_all_text(keyword, links_list)
        print('每经网 '+keyword+' 文本完成')

if __name__ == '__main__':
    main()