import pymysql

db = pymysql.connect(host='localhost', user='root', password='mysql',passwd='mysql',
                     db = 'demo',autocommit=True, #设置修改自动提交到数据库
                     auth_plugin_map='mysql_native_password') #设置身份认证，8.0版本之后建议加上
cursor = db.cursor() #创建一个指针，之后基本所有的操作都是使用指针来实现
cursor.execute('show databases;') #执行SQL语句
db.commit() #将修改提交到数据库——如果连接时参数autocommit设置为false要加上
cursor.fetchall() #获取上一条SQL语句的执行结果，如查询结果等
cursor.fetchone() #获取执行结果的一行
db.close() #关闭数据库
