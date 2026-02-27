本博客将介绍不同出版社的作者排版，介绍时会顺便告知如何标记共一、共同通讯和多个单位。请注意期刊或会议是否允许共一、共同通讯或多个单位，并注意某些“搞特殊的”期刊是否统一使用出版社的通用模板。如果有新的模板，会不断更新哟！另外，以下内容以张三李四王五赵六孙七等举例，邮箱和 ORCID 也是依照名字编的例子，邮箱一般使用单位邮箱（除非单位邮箱很 low），这里先使用 gmail 替代着。如果指向了真实存在的邮箱和 ORCID，恳请联系笔者修正。

---

## Elsevier 出版社下的期刊

最好看的模板，不接受反驳。在 ``\title`` 和 ``\begin{abstract}`` 之间插入作者信息，``\author`` 后的中括号接的是作者单位，支持多单位排版。使用 ``\fnmark[1]`` 标记共同第一作者，使用 ``\cormark[1]`` 标记通讯作者；使用 ``\nonumnote`` 解释通讯记号，使用 ``\fntext[1]`` 解释共一记号。在 Elsevier 模板中，单位会用字母显示，共一会用数字显示。
```
\author[1,2,3]{San Zhang}[orcid=0000-0000-0000-0003]\fnmark[1]
\ead{sanzhang@gmail.com}

\author[1,2]{Si Li}[orcid=0000-0000-0000-0004]\fnmark[1]
\ead{sili@gmail.com}

\author[1]{Wu Wang}[orcid=0000-0000-0000-0005]
\ead{wuwang@gmail.com}

\author[1]{Liu Zhao}[orcid=0000-0000-0000-0006]\cormark[1]
\ead{liuzhao@gmail.com}

\author[1]{Qi Sun}[orcid=0000-0000-0000-0007]\cormark[1]
\ead{qisun@gmail.com}

\address[1]{Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A}
\address[2]{Department/College/School/Faculty/Institute/... B, University B, City B, Country/Region B}
\address[3]{Department/College/School/Faculty/Institute/... C, University C, City C, Country/Region C}

\nonumnote{* These are the corresponding authors. } % \nonumnote{* This is the corresponding author. } 
\fntext[1]{Co-first authors contributed equally to this work. } 
```

---

## Springer 出版社下的期刊

在 ``\title`` 和 ``\maketitle`` 之间放置以下内容，``\inst`` 中标记单位，支持多单位排版。在 ``\inst`` 内，使用 ``\#`` 标记共一，使用 ``*`` 标记通讯。

```
\author{
	San Zhang\inst{1,2,3,\#}
	\and Si Li\inst{1,2,\#}
	\and Wu Wang\inst{1}
	\and Liu Zhao\inst{1,*}
	\and Qi Sun\inst{1,*}
}

\authorrunning{Zhang S et al. }

\institute{
	Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A
	\and Department/College/School/Faculty/Institute/... B, University B, City B, Country/Region B
	\and Department/College/School/Faculty/Institute/... C, University C, City C, Country/Region C
}
```

在 ``\maketitle`` 和 ``\begin{abstract}`` 之间放置以下内容解释共一和共同通讯记号，其中 ``\renewcommand{\thefootnote}{}`` 用于移除 ``\footnotetext`` 自带的标记符。这些命令需要放置在 ``\maketitle`` 后是因为这些命令需要向一个有效的页面添加脚注，如果放在 ``\maketitle`` 前，会有一个含有部分脚注的空白页在正文之前。此处感谢博文 [https://blog.csdn.net/qq_34331113/article/details/121642975](https://blog.csdn.net/qq_34331113/article/details/121642975) 的博主。下文中 ``\url`` 最开始源自 ``\usepackage{url}``，目前建议使用 ``\usepackage{xurl}`` 实现自动换行的 ``\url``（如有需要还可以进一步添加换行处理代码）。读者也可使用 ``\href`` 或者添加 ``mailto:`` 前缀。

```
\renewcommand{\thefootnote}{}
\footnotetext{\textsuperscript{\#} Co-first authors contributed equally to this work. }
\footnotetext{* Corresponding author(s): Liu Zhao (\url{liuzhao@gmail.com}) and Qi Sun (\url{qisun@gmail.com}). }
```

---

## IEEE 会议

在 ``\title`` 和 ``\maketitle`` 之间使用以下内容，其中 ``\linebreakand`` 抄自 [https://blog.csdn.net/lgl123ok/article/details/121033610](https://blog.csdn.net/lgl123ok/article/details/121033610)，需要作者自行根据姓名单位的长短决定在哪里进行换行，有兴趣者可以编写自动排版程式。貌似不支持多单位排版，如果需要可以使用分号硬塞（吧）。另外，如果会议要求移除作者前的序号标记，可以参考 IEEE 期刊排版辅以 ``\thanks`` 命令标记共一。

```
\author{
	\IEEEauthorblockN{1\textsuperscript{st} San Zhang}
	\IEEEauthorblockA{
		\textit{Department/College/School/Faculty/Institute/... A} \\
		\textit{University A} \\
		City A, Country/Region A \\
		\url{sanzhang@gmail.com}
	}
	\and
	\IEEEauthorblockN{1\textsuperscript{st} Si Li}
	\IEEEauthorblockA{
		\textit{Department/College/School/Faculty/Institute/... B} \\
		\textit{University B} \\
		City B, Country/Region B \\
		\url{sili@gmail.com}
	}
	\and
	\IEEEauthorblockN{2\textsuperscript{nd} Wu Wang}
	\IEEEauthorblockA{
		\textit{Department/College/School/Faculty/Institute/... C} \\
		\textit{University C} \\
		City C, Country/Region C \\
		\url{wuwang@e.ntu.edu.sg}
	}
	\linebreakand
	\IEEEauthorblockN{3\textsuperscript{rd} Liu Zhao*}
	\IEEEauthorblockA{
		\textit{Department/College/School/Faculty/Institute/... D} \\
		\textit{University D} \\
		City D, Country/Region D \\
		\url{liuzhao@gmail.com}
	}
	\and
	\IEEEauthorblockN{4\textsuperscript{th} Qi Sun*\thanks{* These are the corresponding authors. }}
	\IEEEauthorblockA{
		\textit{Department/College/School/Faculty/Institute/... E} \\
		\textit{University E} \\
		City E, Country/Region E \\
		\url{qisun@gmail.com}
	}
}
```

另外，如果会议主办方要求移除引用记号外的框框，可以在导言区加入以下代码。

```
\hypersetup{
	colorlinks=false,
	linkbordercolor=white,
	pdfborderstyle={/S/U/W 1}, % remove box
	hidelinks
}
```

调整标题字号为四号加粗可将 ``\title`` 命令作如下修改：

```
\title{\fontsize{12pt}{14.4pt}\selectfont \textbf{Your Title}}
```

若要两栏末尾对齐，则可导入以下宏包：

```
\usepackage{flushend}
```

---

## IEEE 期刊

风格类似于 IEEE 会议，但略有不同。如果使用 IEEE 会议的模板排版 IEEE 期刊，大概率会出问题。另外，IEEE 每个期刊都有自己的一个模板，可从 [https://template-selector.ieee.org/secure/templateSelector/publicationType](https://template-selector.ieee.org/secure/templateSelector/publicationType) 进行选择和下载。此处的作者排版说明将按最大的通用性进行。同理，在 ``\title`` 和 ``\maketitle`` 之间使用以下内容，使用 ``\textsuperscript{\#}`` 标记共一，``*`` 标记通讯作者，``\thanks`` 变成了单位说明（完整句子那种）。

```
\author{
	San Zhang\textsuperscript{\#}\thanks{San Zhang was with the Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A; the Department/College/School/Faculty/Institute/... B, University B, City B, Country/Region B; and the Department/College/School/Faculty/Institute/... C, University C, City C, Country/Region C. }, 
	Si Li\textsuperscript{\#}\thanks{Si Li was with the Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A and the Department/College/School/Faculty/Institute/... B, University B, City B, Country/Region B. }, 
	Wu Wang\thanks{Wu Wang was with the Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A}, 
	Liu Zhao*\thanks{Liu Zhao was with the Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A}, 
	and Qi Sun*\thanks{Qi Sun was with the Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A}
	\thanks{\textsuperscript{\#}San Zhang and Si Li are the co-first authors who contributed equally to this work. }
	\thanks{*Liu Zhao (\protect\url{liuzhao@gmail.com}) and Qi Sun (\protect\url{qisun@gmail.com}) are the corresponding authors. }
}
```

## ACM 会议

类似地，在 ``\title`` 和 ``\maketitle`` 之间使用以下内容。

```
\author{San Zhang\textsuperscript{\#}}
\affiliation{%
	\institution{Department/College/School/Faculty/\\Institute/... A, University A}
	\streetaddress{Street A}
	\city{City A}
	\country{Country/Region A}
}
\email{sanzhang@gmail.com}
\orcid{0000-0000-0000-0003}

\author{Si Li\textsuperscript{\#}}
\affiliation{%
	\institution{Department/College/School/Faculty/\\Institute/... B, University B}
	\streetaddress{Street B}
	\city{City B}
	\country{Country/Region B}
}
\email{sili@gmail.com}
\orcid{0000-0000-0000-0004}

\author{Wu Wang}
\affiliation{%
	\institution{Department/College/School/Faculty/\\Institute/... C, University C}
	\streetaddress{Street C}
	\city{City C}
	\country{Country/Region C}
}
\email{wuwang@gmail.com}
\orcid{0000-0000-0000-0005}

\author{Liu Zhao*}
\affiliation{%
	\institution{Department/College/School/Faculty/\\Institute/... D, University D}
	\streetaddress{Street D}
	\city{City D}
	\country{Country/Region D}
}
\email{liuzhao@gmail.com}
\orcid{0000-0000-0000-0006}

\author{Qi Sun*}
\affiliation{%
	\institution{Department/College/School/Faculty/\\Institute/... E, University E}
	\streetaddress{Street E}
	\city{City E}
	\country{Country/Region E}
}
\email{qisun@gmail.com}
\orcid{0000-0000-0000-0007}

\renewcommand{\shortauthors}{Zhang S, Li S, Wang W, et al. }
```

类似地，在 ``\maketitle`` 和 ``\begin{abstract}`` 之间放置以下内容解释共一和共同通讯记号。

```
\renewcommand{\thefootnote}{}
\footnotetext{\textsuperscript{\#} Co-first authors contributed equally to this work. }
\footnotetext{* Corresponding author(s): Liu Zhao (\url{liuzhao@gmail.com}) and Qi Sun (\url{qisun@gmail.com}). }
```

## Wiley 出版社旗下的刊物

Wiley 的作者单位标记类似于 Elsevier，因此一个作者对应多个单位或一个单位对应多个作者的情况十分容易处理。但相比于 Elsevier，Wiley 似乎没有提供标记共同第一作者的代码。标记共一、共同通讯和共同通讯说明可以考虑使用以下代码，该代码需要放置在 ``\begin{document}`` 后、``\maketitle`` 之前，且建议放置在 ``\title`` 和 ``\titlemark`` 之后。

```
\author[1,2,3]{San Zhang}
\author[1,2]{Si Li}
\author[1]{Wu Wang}
\author[1]{Liu Zhao}
\author[1]{Qi Sun}
\authormark{Zhang S, Li S, Wang W, \textsc{et al.} }

\address[1]{\orgdiv{Department/College/School/Faculty/Institute/... A}, \orgname{University A}, \orgaddress{\state{Street A}, \country{Country A}}}
\address[2]{\orgdiv{Department/College/School/Faculty/Institute/... B}, \orgname{University B}, \orgaddress{\state{Street B}, \country{Country B}}}
\address[3]{\orgdiv{Department/College/School/Faculty/Institute/... C}, \orgname{University C}, \orgaddress{\state{Street C}, \country{Country C}}}

\corres{Corresponding authors: Liu Zhao and Qi Sun \email{liuzhao@gmail.com (Liu Zhao), qisun@gmail.com (Qi Sun)}}
```

使用以下代码实现共一说明（没有符号），放置在 ``\maketitle`` 之后。

```
\renewcommand\thefootnote{}
\footnotetext{San Zhang and Si Li are the co-first authors contributing equally to this work. }
```

## TSP 出版社旗下的刊物

模板风格类似于 Elsevier，出版社模板主动提供共一和通讯的标注方式。在 ``\Title`` 和 ``\abstract`` 之间使用以下内容即可实现共一和共同通讯。

```
\newcommand{\orcidauthorA}{0000-0000-0000-0003}
\newcommand{\orcidauthorB}{0000-0000-0000-0004}
\newcommand{\orcidauthorC}{0000-0000-0000-0005}
\newcommand{\orcidauthorD}{0000-0000-0000-0006}
\newcommand{\orcidauthorE}{0000-0000-0000-0007}

\Author{
	San Zhang\textsuperscript{1,2,3,\#}\orcidA{}, 
	Si Li\textsuperscript{1,2,\#}\orcidB{}, 
	Wu Wang\textsuperscript{1}\orcidC{}, 
	Liu Zhao\textsuperscript{1,*}\orcidD{}, 
	and Qi Sun\textsuperscript{1,*}\orcidE{}
}

\AuthorNames{San Zhang, Si Li, Wu Wang, et al. }

\address{%
	\textsuperscript{1} Department/College/School/Faculty/Institute/... A, University A, City A, Code A, Country A
		
	\textsuperscript{2} Department/College/School/Faculty/Institute/... B, University B, City B, Code B, Country B
	
	\textsuperscript{3} Department/College/School/Faculty/Institute/... C, University C, City C, Code C, Country C
}

\corres{Corresponding Author(s): Liu Zhao and Qi Sun. Email: liuzhao@gmail.com and qisun@gmail.com}

\firstnote{These authors contributed equally to this work} 
\secondnote{}
```

## MDPI 出版社旗下的刊物

模板风格类似于 TSP，出版社模板主动提供共一和通讯的标注方式。在 ``\Title`` 和 ``\abstract`` 之间使用以下内容即可实现共一和共同通讯。

```
\newcommand{\orcidauthorA}{0000-0000-0000-0003} % Add \orcidA{} behind the author's name
\newcommand{\orcidauthorB}{0000-0000-0000-0004} % Add \orcidB{} behind the author's name
\newcommand{\orcidauthorC}{0000-0000-0000-0005} % Add \orcidC{} behind the author's name
\newcommand{\orcidauthorD}{0000-0000-0000-0006} % Add \orcidD{} behind the author's name
\newcommand{\orcidauthorE}{0000-0000-0000-0007} % Add \orcidE{} behind the author's name

\Author{San Zhang$^{1,2,3}$\orcidA{}, Si Li$^{1,2}$\orcidB{}, Wu Wang$^1$\orcidC{}, Liu Zhao$^1$\orcidD{}*, and Qi Sun$^1$\orcidE{}*}

\AuthorNames{San Zhang, Si Li, Wu Wang, Liu Zhao, Qi Sun}

\address{%
	$^{1}$ \quad Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A;\\
	$^{2}$ \quad Department/College/School/Faculty/Institute/... B, University B, City B, Country/Region B;\\
	$^{3}$ \quad Department/College/School/Faculty/Institute/... C, University C, City C, Country/Region C;
}

\corres{Correspondence: liuzhao@gmail.com; qisun@gmail.com; }

\firstnote{Current address: Department/College/School/Faculty/Institute/... A, University A, City A, Country/Region A. }
```

---

## 注意事项

以上内容中，解释共同第一作者和共同通讯作者的文字部分不唯一，笔者可以根据期刊或会议的风格进行修改。邮箱一般使用单位邮箱，除非单位未提供邮箱或单位的邮箱收发系统很差（经常丢失邮件又不会通知）。上述代码风格遵循 LaTeX 缩进，只是笔者本人的喜好，使用时读者可以随意在等效的情况下进行调整和优化。

另外，最近在网络上看到部分作者认为十字架符号表示已故的作者，但在我印象中确实存在一些期刊或会议使用十字架符号来标记共同第一作者，而且 IEEE 期刊模板中直接 ``\IEEEauthorrefmark{2}`` 出来的就是十字架符号。后来问了下图书馆的老师，用井号标记共一的最多，十字架符号次之。若要表示作者已故，使用框框框住名字，而不是标十字架。个人总结了下，标记共同第一作者的符号建议是：Elsevier 模板，用上面的模板，不需要自己指定符号；IEEE 会议模板，直接 1st 或者用十字架符号；IEEE 期刊模板，用十字架符号；其它模板，用井号。如果记性不好或希望完全避免误会，可统一使用井号（代码为 ``\#``）来标记共一（Elsevier 模板和允许 1st 的 IEEE 会议模板除外）。

在修改 ``./Content/title.tex`` 时，Springer 和 Wiley 模板的标题需要手动修改（我也不知道为什么）。

最后，~~因为不方便把编译好的成果拿出来（涉及了具体作者姓名单位和一些未发表的论文），所以没有配图，望大家多多谅解~~~笔者进行了编译，与相应的模板代码一起放置在了 [https://github.com/BatchClayderman/onePaperMultipleTypesettingStyles](https://github.com/BatchClayderman/onePaperMultipleTypesettingStyles) 中。

![加油](https://i-blog.csdnimg.cn/direct/525f61c351ba452bbe4729a14a7581e5.png)

# 加油加油！一切顺利！万事胜意！

愿世间的每一篇论文都能得到应有的尊重，都能去到适合的地方。
