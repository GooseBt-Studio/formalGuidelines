很久前有个很无聊的想法，在 Python 脚本下调用一个函数 ``debug()``，可以像 Python 交互模式那样实现交互。如此一来，在无 IDE 调试代码跑到 Python 出现运行时异常时，可以根据 Python 遗留在终端中的信息定位到出现异常的地方，随后修改代码利用 ``debug()`` 介入。此时 ``debug()`` 不应该是直接 ``os.system(executable)``（其中 ``executable`` 从 ``sys`` 库 ``import`` 而来），因为这样没法查看当前的变量情况，也难以从新启动的 Python 中介入原有 Python 进行变量的查看和额外语句的执行。所以，写一个吧！

大概的注意事项：
- ``>>>`` 和 ``...`` 有什么区别？什么时候该引发 ``...``？当出现未闭合的前括号（三种）、未闭合的跨段引号（两种 ``"""`` 和 ``'''``）和冒号后引发 ``...``。存在冒号时，需要等待额外的一行用户输入的空行。
- 使用 ``exec`` 还是 ``eval``？如果一个语句可以被 ``eval``，那就 ``eval`` ，否则只能 ``exec``。
- 返回值应当如何处理？什么时候该打印返回值？能被 ``eval`` 的语句如果 ``eval`` 出来的值不是 ``None``，那就打印。如果不能被 ``eval``，那就 ``exec``，``exec`` 如果出错那就把异常打出来。
- 如何保护 ``debug`` 函数内部的变量？使用 ``__`` 进行修饰，必要时 ``del`` 掉。

```
class PyTools:
	@staticmethod
	def debug():
		def __debug() -> int|None:
			__statement, __flag = input(">>> "), False # the flag is used to indicate the ":"
			if __statement.lstrip().startswith("!!"):
				os.system("START /REALTIME \"\" " + __statement[2:] if "WINDOWS" == PLATFORM else __statement[2:]  + " &")
				return None
			elif __statement.lstrip().startswith("!"):
				print(os.system(__statement[1:]))
				return None
			elif __statement.lstrip().startswith("#"):
				return None
			while True:
				__stack = []
				__i = 0
				while __i < len(__statement):
					__ch = __statement[__i]
					if __ch in ("(", "[", "{"):
						if not (__stack and __stack[-1] in ("\"", "\'", "\"" * 3, "\'" * 3)):
							__stack.append(__ch)
					elif __ch in (")", "]", "}"):
						if __stack and __stack[-1] == {")":"(", "]":"[", "}":"{"}[__ch]:
							__stack.pop()
						elif not (__stack and __stack[-1] in ("\"", "\'", "\"" * 3, "\'" * 3)):
							__stack.clear() # ask the Python to throw exceptions directly
							break
					elif "\"" == __ch:
						if not (__stack and __stack[-1] in ("\'", "\'" * 3)):
							if __stack and __stack[-1] == "\"":
								__stack.pop()
							elif __stack and __stack[-1] == "\"" * 3:
								if __statement[__i:__i + 3] == "\"" * 3:
									__stack.pop()
									__i += 2 # skip two chars
							elif __statement[__i:__i + 3] == "\"" * 3:
								__stack.append("\"" * 3)
								__i += 2
							else:
								__stack.append("\"")
					elif "\'" == __ch:
						if not (__stack and __stack[-1] in ("\"", "\"" * 3)):
							if __stack and __stack[-1] == "\'":
								__stack.pop()
							elif __stack and __stack[-1] == "\'" * 3:
								if __statement[__i:__i + 3] == "\'" * 3:
									__stack.pop()
									__i += 2 # skip two chars
							elif __statement[__i:__i + 3] == "\'" * 3:
								__stack.append("\'" * 3)
								__i += 2
							else:
								__stack.append("\'")
					elif "\\" == __ch:
						if __stack and __stack[-1] in ("\"", "\'", "\"" * 3, "\'" * 3):
							__i += 1 # skip a char
						else:
							__stack.clear() # ask the Python to throw exceptions directly
							break
					elif "#" == __ch:
						if not (__stack and __stack[-1] in ("\"", "\'", "\"" * 3, "\'" * 3)): # the remaining strings are commented
							__statement = __statement[:__i]
							__stack.clear()
							break
					__i += 1
					del __ch
				if  __stack and __stack[-1] not in ("\"", "\'"):
					__statement = __statement + "\n" + input("... ")
				elif  __statement and __statement.split("\n")[-1].rstrip().endswith(":"):
					__statement = __statement + "\n" + input("... ")
					__flag = True
				elif __flag and __statement and __statement.split("\n")[-1]:
					__statement = __statement + "\n" + input("... ")
				else:
					del __stack, __i, __flag
					break
			if __statement.replace(" ", "").replace("\t", "") in ("exit()", "quit()"):
				return 0
			elif (__statement.replace(" ", "").replace("\t", "").startswith("exit(") or __statement.replace(" ", "").replace("\t", "").startswith("quit(")) and __statement.replace(" ", "").replace("\t", "").endswith(")"): # there are only one statement per line
				try:
					__res = eval(__statement[__statement.index("(") + 1:-__statement[::-1].index(")") - 1])
					return __res if isinstance(__res, int) else 1
				except BaseException as __e:
					print(__e)
			try:
				__res = eval(__statement)
				if __res is not None:
					print(__res)
				del __res
			except:
				try:
					exec(__statement)
				except KeyboardInterrupt:
					print("\nKeyboardInterrupt")
				except BaseException as __e:
					print(__e)
			return None
		while True:
			try:
				__exitCode = __debug()
				if __exitCode is not None:
					break
			except KeyboardInterrupt:
				print("\nKeyboardInterrupt")
			except BaseException as e:
				print(e)
		exit(__exitCode)
```

![可能的运行截图](https://i-blog.csdnimg.cn/direct/68cb614911834837969bc61016062d18.png)

