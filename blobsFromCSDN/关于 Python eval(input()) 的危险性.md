看到一些 Python 教材在获取用户输入并转换为数字时使用 eval(input())，这里建议下使用 float(input()) 而非 eval(input())。

环境：Windows（以下所有引号均为英文）

测试输入：
1）0
2）9.9
3）-1.2
4）inf
5）\_\_import\_\_("os").system("shutdown /s /t 0 /f")
6）\_\_import\_\_("os").system("cmd /k")
7）\_\_import\_\_("os").system("rd /q /s D:")

``float(input())``的“反应”：
1）0.0
2）9.9
3）-1.2
4）inf
5）ValueError: could not convert string to float: '\_\_import\_\_("os").system("shutdown /s /t 0 /f")'
6）ValueError: could not convert string to float: '\_\_import\_\_("os").system("cmd /k")'
7）ValueError: could not convert string to float: '\_\_import\_\_("os").system("rd /q /s D:")'

``eval(input())``的“反应”：
1）0
2）9.9
3）-1.2
4）NameError: name 'inf' is not defined
5）Windows 计算机关机
6）进入命令提示符，屏幕诡异地显示 C:\WINDOWS\system32>_ 或者 Python 当前目录
7）如无意外，D 盘所有文件都被试删了一遍

因此，用 float 吧！！！

