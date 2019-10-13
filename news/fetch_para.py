#根据关键词选出有用的段落 标题也视为一个段落
def fetch_para(text,keyword):
    text_list=text.splitlines()
    #返回字符串列表， 不过分隔符为(’\r’, ‘\r\n’, \n’)，也就是说按照行分隔
    useflu_para=[]
    for e in text_list:
        if keyword in e:
            useflu_para.append(e)
    return useflu_para

with open('/home/cw/文档/event-extra/newdata/每股盈利/124.txt','r',encoding='utf-8') as f1:
    doc=f1.read()

print(fetch_para(doc,'同比'))
