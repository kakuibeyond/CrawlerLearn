import os
import jieba
#去重&分词
#每行的前后加上$ 标记一个语料的开始结束
data_path=r'D:\Projects\CrawlerLearn\newsdata\每经网\事件：盈利亏损'
w_data_path=r'D:\Projects\CrawlerLearn\M事件：盈利亏损M'

# event_list=os.listdir(data_path)
# for event in event_list:
#     len_data=0#该事件有效语料数目
#     os.chdir(w_data_path)
#     try:
#         os.mkdir(event)
#     except:
#         pass
#     event_path = os.path.join(data_path,event)
#     event_path_w = os.path.join(w_data_path,event)
#     print('当前目录：'+event_path)
#     kw_list=os.listdir(event_path)
#     for kw in kw_list:
#         kw_path = os.path.join(event_path,kw)
#         kw_path_w = os.path.join(event_path_w,kw)
#         print('正在处理：'+kw_path)
#         data_list=[]#原始
#         data_list_new=[]#去重 
#         data_list_new_w=[]#去重后分词
#         with open(kw_path,'r',encoding='utf-8') as f1:
#             data_list=f1.readlines()
#             data_list_new=list(set(data_list))#去重
        
#         len_data+=len(data_list_new)
#         print('去重处理完成')
#         with open(kw_path_w,'a+',encoding='utf-8') as f2:
#             for line in data_list_new:
#                 seg_list=jieba.cut(line)
#                 line_w=' '.join(seg_list)
#                 f2.write('$ '+line_w[:-1]+' $\n')
#         print('分词处理完成')
    
    
#     print(event_path+'————去重&分词处理完成')
#     print(event+'语料总数：%d'%(len_data))

kw_list=os.listdir(data_path)
try:
    os.mkdir(w_data_path)
except:
    pass

for kw in kw_list:
    
    kw_path=os.path.join(data_path,kw)

    print('正在读取：'+kw_path)
    data_list=[]#原始
    data_list2=[]#去重
    data_list_w=[]#去标题 分词
    with open(kw_path,'r',encoding='utf-8') as f1:
        data_list=f1.readlines()
        data_list2=list(set(data_list))
    for d in data_list2:
        if '。' in d:#去标题
            seg_list=jieba.cut(d)
            d_w=' '.join(seg_list)
            d_ww='$ '+d_w[:-1]+' $\n'#前后加上$
            data_list_w.append(d_ww)

    w_kw_path=os.path.join(w_data_path,kw)
    try:
        os.mkdir(w_kw_path)
    except:
        pass

    len_list=len(data_list_w)
    os.chdir(w_kw_path)
#效率有点低 后期改
    for num,line in enumerate(data_list_w):#从0开始数
        doc_num=num//20
        end_num=min(doc_num*20+20,len_list)
        doc_name=str(doc_num*20+1)+'-'+str(end_num)+'.txt'
        with open(doc_name,'a+',encoding='utf-8')as f:
            f.write(line)

