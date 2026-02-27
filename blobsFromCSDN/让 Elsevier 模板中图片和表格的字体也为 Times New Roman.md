如题，让 Elsevier 模板中图片和表格的字体也为 Times New Roman。

#### 方法一：仅修改 .tex 文件

使用 pdflatex 引擎：
在导言区添加如下命令：
```
\usepackage{times}
```

使用 XeTeX 或 LuaTeX 引擎：
在导言区添加如下命令：
```
\usepackage{fontspec}
\setmainfont{Times New Roman}
```

#### 方法二：仅修改 .sty 文件
如果不介意修改官方 .sty 文件，可以使用 Ctrl + H 把 cas-common.sty 文件中的 ``\sffamily`` 全部替换成 ``\rmfamily``。

![图片效果图](https://i-blog.csdnimg.cn/direct/61460c1de5bc427198499abd2aa8a3a4.png)
![表格效果图](https://i-blog.csdnimg.cn/direct/dd23c0367c8a441daa28a58df2d1e311.png)


另外一个避坑：使用 \begin{table*} 和 \begin{figure*} 时，建议把 [htbp] 参数去掉哦~
