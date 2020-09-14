page_lists = []
url_left = 'http://news.toocle.com/search/index.php?_d=news&_a=news_search&f=search&terms=%E6%88%98%E7%95%A5%E5%90%88%E4%BD%9C&p='

for i in range(10):
    pre_page = url_left + str(i+1)
    print(pre_page)
    page_lists.append(pre_page)
