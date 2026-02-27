之前说了要做做文件路径类的处理，时间有限就只写了个 Python 版本的。以下是一些坑，按照路径的规则并规避这些坑应该可以在稍微思考后写出来。

- 在 Windows 中，``C:`` 和 ``C:\`` 的含义是不同的。宏观一点而言，Windows 操作系统下一个程序会以一个类似于字典的形式存储每个分区的工作路径。以下以在``C:\Windows\System32`` 下启动 cmd 后执行的一系列命令进行解释，其中参数 ``/D``、``/d`` 含义相同（不区分大小写），路径大小写不敏感。

| **命令** | **含义** | **Python 字典** |
| --- | --- | --- |
| ``cd`` | 查询当前工作目录 | ``{"C:":"\\Windows\\System32"}`` |
| ``cd D:`` | 查询 ``D:``（磁盘驱动器 D:、分区 D、D 盘）上的工作目录 | ``{"C:":"\\Windows\\System32"}`` |
| ``cd "D:\Program Files"`` | 设置或更改 ``D:`` 上的工作目录为 ``"\Program Files"`` | ``{"C:":"\\Windows\\System32", "D:":"\\Program Files"}`` |
| ``cd /d D:`` | 切换程序工作目录至 ``D:`` 上的工作目录（如果未设置 ``D:`` 上的工作目录则默认为根目录 ``\``） | ``{"C:":"\\Windows\\System32", "D:":"\\Program Files"}`` |
| ``cd C:`` | 查询 ``C:`` 上的工作目录 | ``{"C:":"\\Windows\\System32", "D:":"\\Program Files"}`` |
| ``cd /D C:\Windows`` | 设置或更改 ``C:`` 上的工作目录为 ``\Windows`` **并**切换程序工作目录至 ``C:`` 上的工作目录（可见不区分大小写） | ``{"C:":"\\Windows", "D:":"\\Program Files"}`` |
| ``cd C:`` | 查询 ``C:`` 上的工作目录 | ``{"C:":"\\Windows", "D:":"\\Program Files"}`` |
| ``cd C:\`` | 设置或更改 ``C:`` 上的工作目录为根目录 ``\`` **并**切换程序工作目录至该目录（因为程序当前工作目录在 ``C:`` 上） | ``{"C:":"\\", "D:":"\\Program Files"}`` |
| ``cd C:`` | 查询 ``C:`` 上的工作目录 | ``{"C:":"\\", "D:":"\\Program Files"}`` |

![证明](https://i-blog.csdnimg.cn/direct/618a9919a4774d91bb5e0570cdcf1338.png)

- 认为根目录的 ``..`` 依旧指向根目录。直接移除路径中的 ``/./``。直接将若干个路径分隔符合并为一个（抄袭于 Java 特性）。 认为 ``/a/..`` 存在即使根目录下没有 a 这个文件夹（事实上，无论 a 是否真的存在，Python 的 ``os.path.exists("/a/..")`` 都会返回 ``True``，除非在 Windows 中加上 ``/..`` 之后的路径长度超出了 Windows 的最大路径长度）。
- 使用相对路径判断文件是否存在时，以程序当前工作目录作为出发点。在相对路径转绝对路径未提供一个绝对路径作为参考路径时，以程序当前工作目录进行转换，反之亦然。
- 在 Windows 操作系统中，使用路径分隔符（path separator）切割不含盘符的路径得到的若干部分（tokens），如果其中的任一部分（token）满足以下任一条件，则路径非法。
-- 该部分含有不可打印字符（``str.isprintable``）。
-- 该部分含有以下字符中的任意一者：``:*?"<>|``（路径分隔符已在对象实例化和切割的时候消失所以不需要再处理）。
-- 该部分为 Windows 保留文件名（参考自 [https://blog.csdn.net/weixin_33994429/article/details/92154640](https://blog.csdn.net/weixin_33994429/article/details/92154640)）。如需使用可使用 ``\\?\`` 或者内核驱动的特殊形式进行访问，这些内容不在 ``Path`` 类的考虑范围内。
-- 该部分（字符）长度不超过 255，其中无论是单字节字符还是多字节字符长度都算 1（估计是 Windows 内部的编码方式决定的）。
- 在 Windows 操作系统中，路径总长度不超过 32762（由于是用 Python 在自己电脑上测出来的所以不确定是不是通用值）。
- 在非 Windows 操作系统（虽然我最喜欢 Windows 操作系统但它确实很特立独行）中，使用路径分隔符（path separator）切割~~不含盘符的（人家用 mount 本来就没有盘符）~~ 路径得到的若干部分（tokens）中每一部分的字节长度（注意不是字符长度）不能超过 255，可使用 utf-8 转 ``bytes`` 后进行长度的计算，例如 ``len(bytes("我", encoding = "utf-8"))`` 会输出 3。除此之外，只要在路径中不使用 ``'\0'`` 基本都合法（路径分隔符就是路径分隔符）。确实，Linux 等操作系统对路径的限制没有 Windows 的多，而且笔者在自己的 Linux 服务器上递归建立不超过 255 字节的文件夹很久也没见报错。
- 传递受保护属性 dict 时依赖 ``deepcopy`` 进行复制。
- $\cdots$ $\cdots$（看代码吧~）

```
import os
from copy import deepcopy

class Path:
	def __init__(self:object, path:str|object = ".", isWindows:bool = True, workingDirectories:dict = {}) -> object:
		self.__originalPath = str(path) if isinstance(path, (str, Path)) else "."
		self.__isWindows = not (hasattr(isWindows, "__bool__") and not bool(isWindows)) # must be not (A or not B)
		if self.__isWindows and isinstance(workingDirectories, dict): # Windows && parameters passed are valid
			self.__workingDirectories = {}
			for key in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				# Record #
				if key + ":" in workingDirectories:
					self.__workingDirectories[key + ":"] = str(workingDirectories[key + ":"]).replace("/", "\\") if isinstance(workingDirectories[key + ":"], (str, Path)) else "\\"
				elif key.lower() + ":" in workingDirectories:
					self.__workingDirectories[key + ":"] = str(workingDirectories[key.lower() + ":"]).replace("/", "\\") if isinstance(workingDirectories[key.lower() + ":"], (str, Path)) else "\\"
				elif key in workingDirectories:
					self.__workingDirectories[key + ":"] = str(workingDirectories[key]).replace("/", "\\") if isinstance(workingDirectories[key], (str, Path)) else "\\"
				elif key.lower() in workingDirectories:
					self.__workingDirectories[key + ":"] = str(workingDirectories[key.lower()]).replace("/", "\\") if isinstance(workingDirectories[key.lower()], (str, Path)) else "\\"
				else:
					self.__workingDirectories[key + ":"] = "\\"
					continue # this continue stops the recursion
				
				# Uniform #
				if self.__workingDirectories[key + ":"].startswith(key + ":") or self.__workingDirectories[key + ":"].startswith(key.lower() + ":"):
					self.__workingDirectories[key + ":"] = str(Path(self.__workingDirectories[key + ":"][2:], isWindows = self.__isWindows))
				elif self.__workingDirectories[key + ":"].startswith("\\"):
					self.__workingDirectories[key + ":"] = str(Path(self.__workingDirectories[key + ":"], isWindows = self.__isWindows))
				else: # invalid
					self.__workingDirectories[key + ":"] = "\\"
		else:
			self.__workingDirectories = {}
		self.__resolve()
	def __resolve(self:object) -> None:
		# Initialize #
		if self.__isWindows: # Windows
			if (																																							\
				2 == len(self.__originalPath) and ("A" <= self.__originalPath[0] <= "Z" or "a" <= self.__originalPath[0] <= "z") and ":" == self.__originalPath[1]										\
				 or len(self.__originalPath) >= 3and ("A" <= self.__originalPath[0] <= "Z" or "a" <= self.__originalPath[0] <= "z") and ":" == self.__originalPath[1] and "\\" == self.__originalPath[2]		\
			): # starts with a drive letter
				self.__driveLetter = self.__originalPath[0].upper() + ":"
				self.__convertedPath = self.__originalPath[2:].replace("/", "\\")
			else:
				self.__driveLetter = ""
				self.__convertedPath = self.__originalPath.replace("/", "\\")
			self.__sep = "\\"
			self.__reserves = ["CON", "PRN", "AUX", "NUL"] + ["COM{0}".format(i) for i in range(10)] + ["LPT{0}".format(i) for i in range(10)]
		else:
			self.__driveLetter = ""
			self.__convertedPath = self.__originalPath
			self.__sep = "/"
			self.__reserves = []
		
		# Convert #
		if self.__convertedPath:
			# Remove all the repeated path separators #
			vec = list(self.__convertedPath)
			i = 0
			while i < len(vec) - 1: # the length cannot be fixed to speed up here
				if self.__sep == vec[i] and self.__sep == vec[i + 1]:
					del vec[i + 1]
				else:
					i += 1
			self.__convertedPath = "".join(vec)
			
			# merge "." and ".." #
			vec = self.__convertedPath.split(self.__sep)
			i = 1
			while i < len(vec):
				if "." == vec[i]: # we do not remove the first "." here
					del vec[i]
				elif ".." == vec[i]:
					if vec[i - 1] in (".", ".."): # can do nothing if it is "." or ".."
						i += 1
					elif 1 == i and (not vec[0] or 2 == len(vec[0]) and "A" <= vec[0][0] <= "Z" and ":" == vec[0][1]): # ".." of the root is still the root
						del vec[i] # only remove the current ..
					else:
						del vec[i]
						del vec[i - 1]
						i = max(i - 1, 1) # avoid 0
				else:
					i += 1
			if len(vec) >= 2:
				if "." == vec[0] and vec[1]:
					del vec[0]
				self.__convertedPath = self.__sep.join(vec)
			elif 1 == len(vec):
				if vec[0]:
					self.__convertedPath = vec[0]
				else:
					self.__convertedPath = self.__sep
			else:
				self.__convertedPath = "."
			
			# Call strip() for Windows objects #
			#if self.__isWindows:
			#	vec = self.__convertedPath.split(self.__sep)
			#	for i in range(len(vec)):
			#		vec[i] = vec[i].strip()
			#	self.__convertedPath = self.__sep.join(vec)
		else:
			self.__convertedPath = self.__workingDirectories[self.__driveLetter] if self.__isWindows and self.__driveLetter else "."
	def isValid(self:object) -> bool:
		vec = self.__convertedPath.split(self.__sep)
		if self.__isWindows:
			for v in vec:
				if len(v) > 255 or ":" in v or "*" in v or "?" in v or "\"" in v or "<" in v or ">" in v or "|" in v or v.upper() in self.__reserves or not v.isprintable():
					return False
			return len(str(self)) <= 32762 # length
		else:
			for v in vec:
				if "\0" in v or len(bytes(v, encoding = "utf-8")) > 255:
					return False
			return True
	def isAbsolute(self:object) -> bool:
		return self.__convertedPath.startswith(self.__sep)
	def isRelative(self:object) -> bool:
		return not self.__convertedPath.startswith(self.__sep)
	def exists(self:object) -> bool:
		return os.path.exists(str(self))
	def isdir(self:object) -> bool:
		return os.path.isdir(str(self))
	def isfile(self:object) -> bool:
		return os.path.isfile(str(self))
	def islink(self:object) -> bool:
		return os.path.islink(str(self))
	def readlink(self:object) -> str|BaseException:
		try:
			return os.readlink(str(self))
		except BaseException as e:
			return e
	def create(self:object, parameter:None|bool = None) -> None|BaseException:
		path = str(self)
		try:
			if path.endswith(self.__sep) or True == parameter: # create a folder
				os.makedirs(path)
				return None
			else: # create a file
				bRet = Path(self.__sep.join(path.split(self.__sep)[:-1]), isWindows = self.__isWindows).create(True)
				if bRet is None:
					with open(path, "wb") as f:
						return None
				else:
					return  bRet
		except BaseException as e:
			return e
	def setPath(self:object, path:str|object) -> bool:
		if isinstance(path, (str, Path)):
			self.__originalPath = str(path)
			self.__resolve()
			return True
		else:
			return False
	def getPath(self:object) -> str:
		return str(self)
	def setIsWindows(self:object, isWindows:bool) -> bool:
		if hasattr(isWindows, "__bool__"):
			self.__isWindows = bool(isWindows)
			return True
		else:
			return False
	def getIsWindows(self:object) -> bool:
		return self.__isWindows
	def setWorkingDirectory(self:object, key:str, value:str|object) -> bool:
		if self.__isWindows and isinstance(key, str) and isinstance(value, (str, Path)):
			# Set #
			if 1 == len(key) and ("A" <= key <= "Z" or "a" <= key <= "z"):
				realKey = key.upper() + ":"
			elif 2 == len(key) and ("A" <= key[0] <= "Z" or "a" <= key[0] <= "z") and ":" == key[1]:
				realKey = key.upper()
			else:
				return False
			
			# Check #
			self.__workingDirectories[realKey] = str(value)
			if self.__workingDirectories[realKey].startswith(realKey) or self.__workingDirectories[realKey].startswith(realKey.lower()):
				self.__workingDirectories[realKey] = str(Path(self.__workingDirectories[realKey][2:]))
				return True
			elif self.__workingDirectories[realKey].startswith("\\"): # valid
				self.__workingDirectories[realKey] = str(Path(self.__workingDirectories[realKey]))
				return True
			else:
				return False
		else:
			return False
	def setWorkingDirectories(self:object, workingDirectories:dict) -> int:
		if self.__isWindows and isinstance(workingDirectories, dict):
			cnt = 0
			for key, value in workingDirectories.items():
				if self.setWorkingDirectory(key, value):
					cnt += 1
			return cnt
		else:
			return -1
	def getWorkingDirectory(self:object, driveLetter:str) -> str:
		return self.__workingDirectories[driveLetter[0].upper() + ":"] if isinstance(driveLetter, str) and (1 == len(driveLetter) or 2 == len(driveLetter) and ":" == driveLetter[1]) and ("A" <= driveLetter[0] <= "Z" or "a" <= driveLetter[0] <= "z") else None
	def getWorkingDirectories(self:object) -> dict:
		return deepcopy(self.__workingDirectories)
	@staticmethod
	def join(paths:tuple|list, isWindows:bool = True, workingDirectories:dict = {}) -> object:
		vec = []
		for p in paths:
			if hasattr(p, "__str__"):
				vec.append(str(p))
		return Path(("/" if hasattr(isWindows, "__bool__") and not bool(isWindows) else "\\").join(vec), isWindows = isWindows, workingDirectories = workingDirectories)
	@staticmethod
	def abspath(relPath:str|object, currentPath:None|str|object = None, isWindows:bool = True, workingDirectories:dict = {}) -> object:
		if hasattr(relPath, "__str__"):
			p = Path(relPath, isWindows = isWindows, workingDirectories = workingDirectories)
			if p.isAbsolute(): # (ABS, --)
				return p
			elif hasattr(currentPath, "__str__") and Path(currentPath, isWindows = isWindows, workingDirectories = workingDirectories).isAbsolute(): # (REL, ABS)
				Path(currentPath, isWindows = isWindows, workingDirectories = workingDirectories) + relPath
			else: # (REL, REL) or (REL, )
				return Path(os.path.abspath(str(Path(currentPath, isWindows = isWindows, workingDirectories = workingDirectories) + relPath)))
		else:
			return Path(".", isWindows = isWindows, workingDirectories = workingDirectories)
	@staticmethod
	def relpath(absPath:str|object, basePath:str|object, currentPath:None|str|object = None, isWindows:bool = True, workingDirectories:dict = {}) -> object:
		if hasattr(absPath, "__str__") and hasattr(basePath, "__str__"):
			p1, p2 = Path.abspath(absPath, currentPath, isWindows = isWindows, workingDirectories = workingDirectories), Path.abspath(basePath, currentPath, isWindows = isWindows, workingDirectories = workingDirectories)
			try:
				return Path(os.path.relpath(str(p1), str(p2)), isWindows = isWindows, workingDirectories = workingDirectories)
			except BaseException as e:
				return e
		else:
			return Path(".", isWindows = isWindows, workingDirectories = workingDirectories)
	def __add__(self:object, other:str|object) -> object:
		return Path(str(self) + str(other), isWindows = self.__isWindows, workingDirectories = deepcopy(self.__workingDirectories)) if hasattr(other, "__str__") else Path(str(self))
	def __iadd__(self:object, other:str|object) -> None:
		if hasattr(other, "__str__"):
			self.__originalPath += str(other)
			self.__resolve()
	def __str__(self:object) -> str:
		return self.__driveLetter + self.__convertedPath if self.__isWindows and self.__driveLetter else self.__convertedPath
```

![效果图](https://i-blog.csdnimg.cn/direct/21194e62b35f4f60b86a40bf3164dcd5.png)
![效果图](https://i-blog.csdnimg.cn/direct/a686f077b85f4b24a498321777fa0acf.png)
