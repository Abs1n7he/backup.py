import html


str1 = "中文"  #ASCII string
#str = u"中文"  #Unicode string

print('encode编码：', str1.encode('utf-8')  ,  str1.encode('utf-8').decode())                  #\xe6\x88\x91\xe7\x9a\x84\xe5\xa8\x83


print('unicode编码：',str1.encode('unicode-escape').decode(), '\u4e2d\u6587')   #\u6211\u7684\u5a03


print(';'.join(['&#'+str(ord(i)) for i in list(str1)])  ,  html.unescape('&#20013;&#25991;'))

print(';'.join(['&#x'+str(hex(ord(i)))[2:] for i in list(str1)])  ,  html.unescape('&#x4e2d;&#x6587'))

