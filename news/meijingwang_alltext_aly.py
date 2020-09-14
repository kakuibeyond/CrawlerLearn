# -*- coding: utf-8 -*-
#存好结果界面的url列表 然后再放到服务器上面用requests+pyquery爬取

from pyquery import PyQuery as pq
import os
import requests
from requests.exceptions import RequestException
import time

headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5050.400 QQBrowser/10.0.941.400'}

data_path=r'/home/cw/event-extraction/newsdata_alltext'
urllist_path=r'/home/cw/event-extraction/newsdata_alltext/事件：收购重组/result_url_list_qc.txt'
event_name='事件：收购重组'
links_list = []



def get_news_text(url):
    try:
        response = requests.get(url,headers=headers)
        html = response.text
        doc = pq(html)
        title = doc('.g-main .g-article-left .g-article .g-article-top h1').text()
        text = doc('.g-main .g-article .g-articl-text').text()
        whole_text = title+'\n'+text
        return whole_text
    except RequestException:
        print('获取单页文本超时')
        get_news_text(url)


def get_all_text(links_list):
    print('正在获取文本信息')
    
    for num,url in enumerate(links_list):
        if((num)%50==0):
            print('正在处理第%d-%d条信息'%(num+1,num+50))
            os.chdir(data_path+'/'+event_name+'/data')
            newdir='%d-%d'%(num+1,num+50)
            os.mkdir(newdir)
            os.chdir(newdir)
        text = get_news_text(url)
        if not text is None:
            doc_name=str(num+1)+'.txt'
            with open(doc_name,'a',encoding='utf-8') as f1:
                f1.write(text)
        
        time.sleep(1)  # 自定义
            
def main():
    try:
        os.mkdir(data_path)
    except:
        pass
    os.chdir(data_path)

    try:
        os.mkdir(event_name)
    except:
        pass
    os.chdir(event_name)

    try:
        os.mkdir('data')
    except:
        pass
    os.chdir('data')
   
    with open(urllist_path,'r',encoding='utf-8')as furl:
        links_list=furl.readlines()
    
    #去除每个url后面多出的换行符
    links_list2 = [line.replace('\n', '') for line in links_list]


    get_all_text(links_list2)
if __name__ == '__main__':
    main()