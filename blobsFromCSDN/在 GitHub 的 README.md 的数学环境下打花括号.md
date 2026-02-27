在 GitHub 的 README.md 的数学环境下打花括号，使用 LaTeX 方法的 ``$\{a, b, c\} = \{2, 3, 5\}$`` 无效；尝试把 ``$`` 符号放外面  ``{$a, b, c$}$ = ${$2, 3, 5$}``，发现花括号将里面的内容视为纯文本，再次失败；使用 ``\left`` 和 ``\right``，发现 ``$\left{a, b, c\right} = \left{2, 3, 5\right}$`` 和 ``$\left\{a, b, c\right\} = \left\{2, 3, 5\right\}$`` 均无效；随后有人说可以使用 ``$`\{a, b, c`\} = `\{2, 3, 5`\}$``，但依旧无效；最后使用了，``\lbrace`` 和 ``\rbrace``， ``$\lbrace a, b, c\rbrace = \lbrace 2, 3, 5\rbrace$``，成功。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/624e610724184dd5b1aaf855f2550052.png)

