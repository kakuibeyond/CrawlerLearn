import os
#用于在文档每行前后加上'$ ' 和 ' $'

# with open(r'D:\Projects\CrawlerLearn\newsdata\每经网\事件：盈利亏损\亏转盈.txt','r',encoding='utf-8') as f:
#     line=f.readlines()#读出来的每一行包含最后的换行符\n
#     print('$ '+line[0][0:-1])+' $')#去掉换行符  前后加上$

path_w=r'C:\Users\56386\Desktop\事件：盈利亏损'
path_w_h=r'C:\Users\56386\Desktop\盈利亏损原始语料'
for kw in os.listdir(path_w):
    file_path=os.path.join(path_w,kw)
    with open(file_path,'r',encoding='utf-8')as f0:
        list_line=f0.readlines()
    file_path_h=os.path.join(path_w_h,kw)
    with open(file_path_h,'a+',encoding='utf-8')as f1:
        for line in list_line:
            f1.write('$ '+line[:-1]+' $\n')



