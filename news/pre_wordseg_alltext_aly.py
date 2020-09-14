import os
import jieba
#分词

#for aliyun linux
data_path=r'/home/cw/event-extraction/newsdata_alltext/事件：收购重组/data'
data_path_w=r'/home/cw/event-extraction/newsdata_alltext/事件：收购重组/data_w'

# for Windows
# data_path=r'D:\Projects\CrawlerLearn\newsdata_alltext\事件：收购重组\data'
# data_path_w=r'D:\Projects\CrawlerLearn\newsdata_alltext\事件：收购重组\data_w'

dirlists=os.listdir(data_path)
try:
    os.mkdir(data_path_w)
except:
    pass

os.chdir(data_path_w)
for dir in dirlists:
    os.mkdir(dir)
os.chdir(data_path)
for dir in dirlists:#1-50  51-100等
    filepath=os.path.join(data_path,dir)#data/1-50/
    filepath_w=os.path.join(data_path_w,dir)#data_w/1-50/
    print('正在处理目录：'+filepath)
    os.chdir(filepath)
    for file in os.listdir(filepath):
        filename=os.path.join(filepath,file)#文件全路径
        with open(filename,'r',encoding='utf-8') as f1:
            alltext=f1.read().replace('\n','')#去掉换行符
        
        seg_list=jieba.cut(alltext)
        line_w=' '.join(seg_list)
        filename_w=os.path.join(filepath_w,file)#文件分词后全路径
        with open(filename_w,'a',encoding='utf-8') as f2:
            f2.write(line_w)
    print('目录处理完成：'+filepath)


