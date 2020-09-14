listurl=[]
with open(r'D:\Projects\CrawlerLearn\newsdata_alltext\事件：收购重组\result_url_list.txt','r',encoding='utf-8')as f:
    listurl=f.readlines()
    print(listurl[0])
    print(listurl[1])

    print(len(listurl))
    listurl=list(set(listurl))
    print(len(listurl))
with open(r'D:\Projects\CrawlerLearn\newsdata_alltext\事件：收购重组\result_url_list_qc.txt','a+',encoding='utf-8')as f2:
    for line in listurl:
        f2.write(line)#自带换行符

