#测试去重&分词
import jieba
import os

file_path=r'D:\Projects\CrawlerLearn\newsdata_alltext\事件：收购重组\data\12.txt'
file_path_w=r'D:\Projects\CrawlerLearn\newsdata_alltext\事件：收购重组\data_w\12w_new.txt'

with open(file_path,'r',encoding='utf-8') as f1:
    alltext=f1.read().replace('\n','')
seg_list=jieba.cut(alltext)
line_w=' '.join(seg_list)
with open(file_path_w,'a',encoding='utf-8') as f2:
    f2.write(line_w)

print('分词处理完成')

