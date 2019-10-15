import os
import jieba
#去重&分词
data_path=r'D:\Projects\CrawlerLearn\newsdata\每经网'
w_data_path=r'D:\Projects\CrawlerLearn\newsdata_w\每经网'

event_list=os.listdir(data_path)
for event in event_list:
    len_data=0#该事件有效语料数目
    os.chdir(w_data_path)
    try:
        os.mkdir(event)
    except:
        pass
    event_path = os.path.join(data_path,event)
    event_path_w = os.path.join(w_data_path,event)
    print('当前目录：'+event_path)
    kw_list=os.listdir(event_path)
    for kw in kw_list:
        kw_path = os.path.join(event_path,kw)
        kw_path_w = os.path.join(event_path_w,kw)
        print('正在处理：'+kw_path)
        data_list=[]#原始
        data_list_new=[]#去重
        data_list_new_w=[]#去重后分词
        with open(kw_path,'r',encoding='utf-8') as f1:
            data_list=f1.readlines()
            data_list_new=list(set(data_list))
        
        len_data+=len(data_list_new)
        print('去重处理完成')
        with open(kw_path_w,'a+',encoding='utf-8') as f2:
            for line in data_list_new:
                seg_list=jieba.cut(line)
                line_w=' '.join(seg_list)
                f2.write(line_w)
        print('分词处理完成')
    
    
    print(event_path+'————去重&分词处理完成')
    print(event+'语料总数：%d'%(len_data))

