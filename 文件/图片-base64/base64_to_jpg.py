# 二进制方式打开图片文件
import base64


txt = open(r"base64.txt", "rb")

str1 = str(txt.read(),'utf-8')
print(str1)


if (len(str1)%4 == 1): #当原数据长度不是4的整数倍时，在编码结果后加1到3个=
	str1 += "==="
elif (len(str1)%4 == 2):
	str1 += "=="
elif (len(str1)%4 == 3):
	str1 += "="

jpg = open(r"jpg.jpg","wb+")
jpg.write(base64.b64decode(str1.encode('utf-8')))
jpg.close()
txt.close()
print("输入：base64.txt")
print("输出：jpg.jpg")
