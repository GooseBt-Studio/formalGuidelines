要缩小模板标题和作者信息之间的间距，在 \title{} 内的结尾处加上 \vspace{-0.5em} 可实现调整，负数绝对值越大缩小的距离越多，更多方法可参考 [https://resourceful.github.io/latex/acm/usenix/template/2016/09/22/LaTeX-text-below-title/](https://resourceful.github.io/latex/acm/usenix/template/2016/09/22/LaTeX-text-below-title/)。

要缩小作者信息和正文之间的间距，在导言区（\begin{document} 前）放入以下内容，其中第一个数值 ``0.5`` 不需要修改，第二个数值 ``-1`` 的绝对值越大缩小的距离越多。更多方法可参阅 [https://tex.stackexchange.com/questions/166221/how-to-reduce-space-after-authors-block-ieeetran](https://tex.stackexchange.com/questions/166221/how-to-reduce-space-after-authors-block-ieeetran)。

```
\makeatletter
\patchcmd{\@maketitle}
  {\addvspace{0.5\baselineskip}\egroup}
  {\addvspace{-1\baselineskip}\egroup}
  {}
  {}
\makeatother
```

注意，以上缩小的原理，其实是把后面那部分内容往前提，不是真正意义上的缩小，过大的负数绝对值可能导致后面部分的内容与前面部分的内容重叠，甚至越界。调整后，需要编译查看数值是否合适，并做适当调整。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/71ea8efbc43e4438ac23f4d856a6a9b7.png)

