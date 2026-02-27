在 LaTeX 中，一稿多版（一篇论文多个排版）模式是十分好用的，尤其对频繁被无理由拒稿需要不停切换期刊甚至是出版社的作者而言，该排版模式能够大大地加速重排版和重投稿效率。~~希望学术界在很久以后允许一稿多投或跨出版社自动迁移免得浪费投稿时间（投稿总耗时比做研究或写论文的耗时还多），身边的人都在说别人“就那么缺论文吗？”自己却更是缺论文缺到到处找挂名。~~ 

![一稿多版文件夹结构](https://i-blog.csdnimg.cn/direct/0665ea4c6cc54eb894b57a0898bd4470.png)
由于不同出版社对 Abstract 和 Keyword 的排版要求不同，一般情况下，我们会将 Abstract 的文本（不包括 begin 和 end 部分）抽离出来。然而，在 Elsevier 模板中，以下代码却不可用。

```
\begin{abstract}
	\input{../Content/abstract.tex}
\end{abstract}
```
![错误排版](https://i-blog.csdnimg.cn/direct/0a66973046b4408a9ea751c0c19dfbdc.png)
网上搜了一圈，没找到方法，于是自己动手尝试。不断尝试发现，假如将 ``\input{../Content/abstract.tex}`` 改成 ``a\input{../Content/abstract.tex}``，就可以把整段摘要文本读取进来，但是会出现一个额外的字母 ``a``。于是，考虑使用 ``%`` 符号，在 ``\begin{abstract}`` 和 ``\input{../Content/abstract.tex}`` 后面都加上一个百分号，发现无济于事。最后，试出了在 ``\input{../Content/abstract.tex}`` 前加一个 ``\ `` （反斜杠空格）的办法，编译后摘要文本正常显示且前方没有额外的空格。

```
\begin{abstract}
	\ \input{../Content/abstract.tex}
\end{abstract}
```
![正确排版](https://i-blog.csdnimg.cn/direct/71e715edb78e4f0e9a0281dba360e71d.png)
最后，希望大家都能顺顺利利地把自己辛辛苦苦做的科研成果发到自己想要的地方！
