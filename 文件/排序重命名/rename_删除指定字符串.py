import os
import re

##############删除文件名中指定字符串

thedir = r'E:\摄影\人像\17.07.19 柳欣怡\jpg'
os.chdir(thedir)

temp={}
for root,dirs,files in os.walk(thedir):
    print(files)
    for f in files:
        try:
            newname = re.findall(re.compile('(.*?) 拷贝.jpg', re.S), f)[0]
            print("%s\t改为 %s" %(f,newname+'.jpg'))
            temp[f]=newname+'.jpg'
        except:pass

# for key,value in temp.items():
#     os.rename(key,value)

