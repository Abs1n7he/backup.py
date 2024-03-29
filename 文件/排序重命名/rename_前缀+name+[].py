import os
import re
i = 1


thedir = r'D:\Download\白莉爱吃巧克力'
os.chdir(thedir)
dict={}

#########################前缀+name+[] 格式的名称，改为name

first='白莉爱吃巧克力'#前缀
for item in os.scandir(thedir):
    if item.is_dir():
        oldname=os.path.basename(item.path)
        try:
            newname = re.findall(re.compile(first+r'\s(.*?)\s\[', re.S), oldname)[0]        #前缀+name+[]
            print('{: <40s}'.format(oldname)+'修改为： '+newname)  #abc#####
            os.rename(oldname, newname)
        except:
            print('error: '+oldname)


# for item in os.scandir(thedir):
#     if item.is_dir():
#         oldname=os.path.basename(item.path)
#         try:
#             newname = oldname.partition(' ')[2]
#             print('{: <40s}'.format(oldname)+'修改为： '+newname)                         #空格分割
#             os.rename(oldname, newname)
#         except:
#             print('error: '+oldname)
