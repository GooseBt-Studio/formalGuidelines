大家都知道字符串的转义，即，若想在 Python 中表达由一个反斜杠组成的字符串，需要使用 ``"\\"`` ~~或 ``r"\"``~~ 来进行表达。在 ``"\\"`` 中，前面的反斜杠表示对后面的反斜杠进行转义，即告知 Python 后面的反斜杠是一个普通字符。那么，有些时候，我们需要将信息以 Python 字符串的形式抛给用户，就很可能要用到反向转义了。例如，我们希望将从文件读取上来的一些含有换行符、制表符等的内容在控制台中直接用一个 Python 字符串的形式告诉用户，就需要反向转义。事实上，这就是相当于能够把从其它地方读取过来的字符串以不换行的字符串的形式直接粘贴到 Python 交互模式下并被 Python 解释器成功解析。

思路大致是，先判断是否存在一些常用的字符，参考自 [https://blog.csdn.net/any1where/article/details/132859406](https://blog.csdn.net/any1where/article/details/132859406)，随后将不可打印字符转为十六进制，用 ``"\\x"`` 替换 ``"0x"`` 前缀完成反向转义。以对 ``string`` 的处理为例，一个可能的代码如下。

```
def convertEscaped(string:str) -> str:
	if isinstance(string, str):
		vec = list(string)
		d = {"\\":"\\\\", "\"":"\\\"", "\'":"\\\'", "\a":"\\a", "\b":"\\b", "\f":"\\f", "\n":"\\n", "\r":"\\r", "\t":"\\t", "\v":"\\v"}
		for i, ch in enumerate(vec):
			if ch in d:
				vec[i] = d[ch]
			elif not ch.isprintable():
				vec[i] = "\\x" + hex(ord(ch))[2:]
		return "\'" + "".join(vec) + "\'"
	else:
		return str(string)
```

![效果图](https://i-blog.csdnimg.cn/direct/6a30656b97fe4d208fcfcdd996b00344.png)
没错，第一个打印出来的 ``'\n'``，是一个实实在在的 ``"\'\\n\'"``。
