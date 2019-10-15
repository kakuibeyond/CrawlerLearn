#测试去重&分词
import jieba
import os

file_path=r'D:\Projects\CrawlerLearn\newsdata\每经网\事件：盈利亏损\亏转盈.txt'
file_path_q=r'D:\Projects\CrawlerLearn\亏转盈_q.txt'
file_path_qw=r'D:\Projects\CrawlerLearn\亏转盈_w.txt'
data_list=[]
data_list_new=[]
data_list_new_w=[]
with open(file_path,'r',encoding='utf-8') as f1:
    data_list=f1.readlines()
data_list_new=list(set(data_list))
with open(file_path_q,'a+',encoding='utf-8') as f2:
    for line in data_list_new:
        f2.write(line)
print('去重处理完成')
with open(file_path_qw,'a+',encoding='utf-8') as f3:
    for line in data_list_new:
        seg_list=jieba.cut(line)
        line_w=' '.join(seg_list)
        f3.write(line_w)
print('分词处理完成')

