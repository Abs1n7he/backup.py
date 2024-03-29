import time
print('当前时间:',time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time.time())))
print('当前时间戳:',time.time())
print('1.时间转时间戳/2.时间戳转时间')
switch1=input('>>')

if switch1=='1':
	print('1.时间转时间戳:')
	while True:
		try:
			time1=input('>>')
			print(int(time.mktime(time.strptime(time1, "%Y/%m/%d %H:%M:%S"))))
		except:
			break
elif switch1=='2':
	print('2.时间戳转时间:')
	while True:
		try:
			time2=float(input('>>'))
			print(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(time2)))
		except:
			break

#时间戳一天就是+86400
