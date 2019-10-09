import urllib.request

# from selenium import webdriver
# browser = webdriver.Chrome()

resp1=urllib.request.urlopen("http://www.baidu.com")
str1 = resp1.read()
print(len(str1))

resp2=urllib.request.Request("http://www.baidu.com")
resp2.add_header('Host','www.baidu.com')
r = urllib.request.urlopen(resp2)#上面的打开网址连接是一样的，只是把网址换成了Request对象
str2 = r.read()
print(len(str2))#str2加上了头部，length比str1略大
