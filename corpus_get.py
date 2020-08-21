from urllib import request
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import re
f=open('corpus/songbie.txt','a+',encoding='utf-8')
for i in range(1,7):#翻页
    typemain='1A51542a43c484A'#爬什么类型的诗
    url='https://so.gushiwen.org/shiwen/default_'+typemain+str(i)+'.aspx'
    headers ={
            "User-Agent":UserAgent().chrome
    }
    req=request.Request(url,headers=headers)
    resp=request.urlopen(req)
    html_data=resp.read().decode()
    soup=bs(html_data,'html.parser')
    #print(html_data)
    title_all=soup.find_all('b')#全部的标题
    contson_all=soup.find_all('div',class_='contson')#全部的内容
    for j in range(0,9):
        f.write(title_all[j].get_text().replace('\n', '').replace('　', '')+'::'+contson_all[j].get_text().replace('\n', '').replace('　', '')+'\n')
#要记得格式化数据，此时一首诗占一行
#and为什么要用：：？因为古诗中也会用到冒号，所以我们用：：
        #print(title_all[i].get_text())
        #print(contson_all[i].get_text())
f.close()
