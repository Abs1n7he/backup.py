# 二进制方式打开图片文件
import base64
jpgfile = input('jpg:')
jpg = open(jpgfile, "rb")

#读取文件的内容转换为base64编码str(base64.b64encode(str1.encode('utf-8')),'utf-8')
jpgbase64 = str(base64.b64encode(jpg.read()),'utf-8')
txt = open(r"base64.txt","w+")
txt.write(jpgbase64)
print(jpgbase64)
jpg.close()
txt.close()
print("输出：base64.txt")