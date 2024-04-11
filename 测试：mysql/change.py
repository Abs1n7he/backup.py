import pymysql
import pandas as pd

# 连接数据库
connection = pymysql.connect(host='localhost', user='root', password='fyp734',db = 'test',cursorclass=pymysql.cursors.DictCursor,auth_plugin_map='mysql_native_password') #设置身份认证，8.0版本之后建议加上

sql="select * from table1"
key='id'#主键

# 执行第一次查询
with connection.cursor() as cursor:
    cursor.execute(sql)
    result1 = cursor.fetchall()

wait=input("waiting...")
# 执行第二次查询
with connection.cursor() as cursor:
    cursor.execute(sql)
    result2 = cursor.fetchall()

# result1=[{'id': 1, 'name': 'tom', 'age': 1}, {'id': 2, 'name': 'toy', 'age': 2}, {'id': 3, 'name': 'sub', 'age': 3}]
# result2=[{'id': 1, 'name': 'tom', 'age': 1}, {'id': 2, 'name': 'toy', 'age': 20}, {'id': 4, 'name': 'qq', 'age': 1}, {'id': 5, 'name': 'qq', 'age': 1}]

# 转换为DataFrame
df1 = pd.DataFrame(result1)
df2 = pd.DataFrame(result2)

# 设置主键
df1.set_index(key, inplace=True)
df2.set_index(key, inplace=True)

# 比较数据
add     = df2[~df2.index.isin(df1.index)]       #新增：在df2里排除掉：在df2且在df1的
delete  = df1[~df1.index.isin(df2.index)]       #删除：在df1里排除掉：在df1且在df2的
temp    = df1[df1.isin(df2)].dropna()           #不变：
update1 = df1[~df1.isin(temp)&~df1.isin(delete)].dropna()   #修改前：在df1里排除掉：df1里不变和删除
update2 = df2[~df1.isin(temp)].dropna()                     #修改后：在df2里排除掉：df1里不变


# 将结果输出到Excel中的三个不同的sheet中
with pd.ExcelWriter('result.xlsx') as writer:
    add.to_excel(writer, sheet_name='新增')
    delete.to_excel(writer, sheet_name='删除')
    update1.to_excel(writer, sheet_name='修改前')
    update2.to_excel(writer, sheet_name='修改后')

# 关闭数据库连接
connection.close()