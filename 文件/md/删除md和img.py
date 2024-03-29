import re
import os



file=r'D:\work\tool\github\Struts2scan\readme.md1'


f= open(file, 'r', encoding='utf-8')
for line in f:
   line = line.strip()     # 过滤杂质

   if re.findall('!\[(.*?)\]\((.*?)\)', line):                 #![](img/30.jpg)
      temp=re.findall(re.compile(r'\((.*?)\)', re.S), line)
      for i in temp:                                     #防止一行两个图片的情况
         delfile=os.path.join(os.path.dirname(file), i) #当前目录和md里图片目录拼接
         try:
            os.remove(delfile)
            print('已删除：',delfile)
         except:
            print('不存在：',delfile)

   elif re.findall('<img src="(.*?)"', line):                  #<img src="img/10.jpg" style="zoom:50%;" />
      temp=re.findall(re.compile(r'src="(.*?)\"', re.S), line)
      for i in temp:
         delfile=os.path.join(os.path.dirname(file), i)
         try:
            os.remove(delfile)
            print('已删除：',delfile)
         except:
            print('不存在：',delfile)
         
f.close()
os.remove(file)
print('已删除：',file)



