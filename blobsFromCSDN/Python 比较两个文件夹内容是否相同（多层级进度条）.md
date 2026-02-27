以下代码实现 Python 比较两个文件夹内容是否相同，命名为``compareDirectory.py``。
该代码的优势在于：
1）通过层次遍历法跳过一些不同步的文件夹从而避免遍历不同步文件夹内的内容来达到剪枝的效果（花了一个晚上）；
2）参阅了某 ACM 大佬关于比较版本号的算法，使用过程中的 ``list.pop(0)`` 和结尾处的 ``not any`` 进行加速运算（花了十分钟左右吧）；
3）报告相对路径、增删情况等（花了一分钟左右吧）；
4）通过 SHA256 哈希值比较文件内容，与逐字节对比相比，虽然两者都需要遍历整个文件，但使用哈希函数的方法通过节省了 if 的执行数量（哈希值往往更短且生成哈希与比较哈希的时间之和往往少于逐字节比较的时间）来达到节省时间的目的（花了一分钟左右吧）；
5）拥有多层级进度报告结构（貌似这个功能花费的时间和前面四点之和一样）。

完整代码如下：

```
import platform
import os
from sys import stdin, exit
from shutil import copy, copytree, rmtree
import hashlib
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)
specialFolders = ["", ".", ".."]
ncols = 100


class ProgressBar:
	def __init__(self:object, total:int, desc:str = "", postfix:str = "", ncols:int = 100) -> object:
		self.c = 0
		self.total  = total
		self.desc = str(desc)
		self.postfix = str(postfix)
		self.ncols = ncols
		self.print()
	def update(self:object, c:int) -> bool:
		if isinstance(c, int) and c >= 0:
			self.c += c
			self.print()
			return True
		else:
			return False
	def set_postfix(self:object, postfix:str) -> None:
		self.postfix = str(postfix)
	def print(self:object) -> None:
		print("\r" + str(self), end = "")
	def __str__(self:object) -> str:
		try:
			return "{0}: {1} / {2} = {3:.2f}% {4}".format(self.desc, self.c, self.total, 100 * self.c / self.total if self.c >= 0 and self.total > 0 else float("nan"), self.postfix)[:self.ncols]
		except:
			return ""


def clearScreen(fakeClear:int = 120):
	if stdin.isatty(): # is at a console
		if platform.system().lower() == "windows":
			os.system("cls")
		elif platform.system().lower() == "linux":
			os.system("clear")
		else:
			try:
				print("\n" * int(fakeClear))
			except:
				print("\n" * 120)
	else:
		try:
			print("\n" * int(fakeClear))
		except:
			print("\n" * 120)

def SHA256(fpath:str, isEcho:bool = False) -> str|Exception|None:
	if not os.path.isfile(fpath):
		return None
	try:
		with open(fpath, "rb") as f:
			hash = hashlib.new("SHA256")
			for chunk in iter(lambda: f.read(1 << 20), b""):
				hash.update(chunk)
			return hash.hexdigest()
	except Exception as e:
		if isEcho:
			print("\"{0}\" -> {1}".format(fpath, e))
		return e

def compare(rootDir1:str, rootDir2:str, dir1:str, dir2:str, compareFileContent:bool = True, caseSensitive:bool = True, indent:int = 0, flags:list = [True]) -> tuple:
	addLists, removeLists, conflictLists, exceptionLists, differLists = [], [], [], [], []
	try:
		listDir1, listDir2 = sorted([item for item in os.listdir(dir1) if item not in specialFolders]), sorted([item for item in os.listdir(dir2) if item not in specialFolders]) # 获取一层并排除特殊的文件夹
	except Exception as e:
		exceptionLists.append((os.path.relpath(dir1, rootDir1), e))
		print("\r" + " " * ncols + "\x1b[F\x1b[K", end = "") # 向上一层
		return (addLists, removeLists, conflictLists, exceptionLists, differLists)
	pBar = ProgressBar(total = len(listDir1) + len(listDir2), desc = "Layer {0}".format(indent), postfix = "(a, r, c, e, d) = (0, 0, 0, 0, 0)", ncols = ncols)
	try:
		while listDir1 and listDir2:
			if listDir1[0] == listDir2[0] or not caseSensitive and listDir1[0].lower() == listDir2[0].lower(): # 相同情况比较属性（目录或文件）是否一致
				target1, target2 = os.path.join(dir1, listDir1[0]), os.path.join(dir2, listDir2[0])
				if os.path.isdir(target1) and os.path.isdir(target2): # 都是文件夹则递归
					print() # 向下一层
					tRet = compare(rootDir1, rootDir2, target1, target2, compareFileContent = compareFileContent, caseSensitive = caseSensitive, indent = indent + 1, flags = flags)
					addLists.extend(tRet[0])
					removeLists.extend(tRet[1])
					conflictLists.extend(tRet[2])
					exceptionLists.extend(tRet[3])
					differLists.extend(tRet[4])
					del tRet # 手动释放内存
					if not flags[0]:
						raise KeyboardInterrupt
				elif os.path.isfile(target1) and os.path.isfile(target2): # 都是文件
					if compareFileContent:
						sha1 = SHA256(target1)
						sha2 = SHA256(target2)
						if isinstance(sha1, str) and isinstance(sha2, str):
							if sha1 != sha2:
								differLists.append(os.path.relpath(target1, rootDir1))	
						else:
							exceptionLists.append((os.path.relpath(target1, rootDir1), (sha1, sha2)))
				else: # 属性（目录或文件）不同
					conflictLicts.append(os.path.relpath(target1, rootDir1))
				listDir1.pop(0)
				listDir2.pop(0)
				pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(addLists), len(removeLists), len(conflictLists), len(exceptionLists), len(differLists)))
				pBar.update(2)
			elif listDir1[0] < listDir2[0]: # 第一个目标小
				target1 = os.path.join(dir1, listDir1[0])
				removeLists.append(os.path.relpath(target1, rootDir1)) # 标记为删除
				listDir1.pop(0)
				pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(addLists), len(removeLists), len(conflictLists), len(exceptionLists), len(differLists)))
				pBar.update(1)
			elif listDir1[0] > listDir2[0]: # 第二个目标小
				target2 = os.path.join(dir2, listDir2[0])
				addLists.append(os.path.relpath(target2, rootDir2)) # 标记为增加
				listDir2.pop(0)
				pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(addLists), len(removeLists), len(conflictLists), len(exceptionLists), len(differLists)))
				pBar.update(1)
		if listDir1:
			removeLists.extend([os.path.relpath(os.path.join(dir1, item), rootDir1) for item in listDir1])
			pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(addLists), len(removeLists), len(conflictLists), len(exceptionLists), len(differLists)))
			pBar.update(len(listDir1))
		elif listDir2:
			addLists.extend([os.path.relpath(os.path.join(dir2, item), rootDir2) for item in listDir2])
			pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(addLists), len(removeLists), len(conflictLists), len(exceptionLists), len(differLists)))
			pBar.update(len(listDir2))
		print("\r" + " " * ncols + "\x1b[F\x1b[K", end = "") # 向上一层
	except KeyboardInterrupt:
		flags[0] = False
	return (addLists, removeLists, conflictLists, exceptionLists, differLists)

def selectOperation(addFlag:bool, removeFlag:bool, differFlag:bool) -> int:
	print("\n可供选择的操作如下（“删除”指直接删除而非移至回收站）：")
	if addFlag:
		print("\t1 = 从目标文件夹删除目标文件夹拥有而源文件夹没有的文件（源 → 目标）")
		print("\t2 = 从目标文件夹向源文件夹复制目标文件夹拥有而源文件夹没有的文件（目标 → 源）")
	if removeFlag:
		print("\t3 = 从源文件夹向目标文件夹复制源文件夹拥有而目标文件夹没有的文件（源 → 目标）")
		print("\t4 = 从源文件夹删除源文件夹拥有而目标文件夹没有的文件（目标 → 源）")
	if differFlag:
		print("\t5 = 从源文件夹向目标文件夹同步内容不同的文件（源 → 目标）")
		print("\t6 = 从目标文件夹向源文件夹同步内容不同的文件（目标 → 源）")
	print("\t7 = 保存对比结果")
	print("\t8 = 重新发起检查（原有配置）")
	print("\t9 = 发起新的检查")
	print("\t0 = 退出程序")
	print()
	iRet = input("请选择一项以继续：")
	while True:
		if iRet in (str(i) for i in range(10)):
			if iRet in "7890" or input("即将执行操作 {0}，为确保不是误触，请输入“Y”（区分大小写）回车以再次确认：".format(iRet)) == "Y":
				return int(iRet)
			else:
				iRet = input("输入取消，请重新输入：")
		else:
			iRet = input("无效输入，请重试：")

def doRemove(folder:str, targetList:list) -> bool:
	successCnt, totalCnt = 0, 0
	for item in targetList:
		totalCnt += 1
		toRemoveFp = os.path.join(folder, item)
		try:
			if os.path.isdir(toRemoveFp):
				rmtree(toRemoveFp)
			else:
				os.remove(toRemoveFp)
			successCnt += 1
		except Exception as e:
			print("Failed removing \"{0}\". Details are as follows. \n{1}".format(toRemoveFp, e))
	print("删除完成，删除成功率：{0} / {1} = {2}%。".format(successCnt, totalCnt, 100 * successCnt / totalCnt)) # 不存在 0 除情况
	return successCnt == totalCnt

def doCopy(dir1:str, dir2:str, targetList:list) -> bool:
	successCnt, totalCnt = 0, 0
	for item in targetList:
		totalCnt += 1
		sourceFp = os.path.join(dir1, item)
		targetFp = os.path.join(dir2, item)
		try:
			if os.path.isdir(sourceFp):
				copytree(sourceFp, targetFp)
			else:
				copy(sourceFp, targetFp)
			successCnt += 1
		except Exception as e:
			print("Failed copying \"{0}\" to \"{1}\". Details are as follows. \n{2}".format(sourceFp, targetFp, e))
	print("复制完成，复制成功率：{0} / {1} = {2}%。".format(successCnt, totalCnt, 100 * successCnt / totalCnt)) # 不存在 0 除情况
	return successCnt == totalCnt

def doCompare(dir1:str, dir2:str, compareFileContent:bool = True, caseSensitive:bool = True, state:list = [True]) -> bool:
	clearScreen()
	if not os.path.isdir(dir1):
		print("源文件夹不存在：\"{0}\"\n请按回车键返回。".format(dir1))
		input()
		return None
	elif not os.path.isdir(dir2):
		print("目标文件夹不存在：\"{0}\"\n请按回车键返回。".format(dir2))
		input()
		return None
	elif dir1 == dir2 or not caseSensitive and dir1.lower() == dir2.lower():
		print("源文件夹路径和目标文件夹路径相同，请按回车键返回。")
		input()
		return None
	else:
		print("源文件夹：\"{0}\"".format(dir1))
		print("目标文件夹：\"{0}\"".format(dir2))
		print()
		flags = [True]
		addLists, removeLists, conflictLists, exceptionLists, differLists = compare(dir1, dir2, dir1, dir2, compareFileContent = compareFileContent, caseSensitive = caseSensitive, flags = flags)
		if not flags[0]:
			print("\nThe process is interrupted by users. ")
		print()
		print("addLists = {0}".format(addLists))
		print("removeLists = {0}".format(removeLists))
		print("conflictLists = {0}".format(conflictLists))
		print("exceptionLists = {0}".format(exceptionLists))
		if compareFileContent:
			print("differLists = {0}".format(differLists))
			print("Totally {0} added, {1} removed, {2} conflicted, {3} erroneous, and {4} different items. ".format(len(addLists), len(removeLists), len(conflictLists), len(exceptionLists), len(differLists)))
		else:
			print("Totally {0} added, {1} removed, {2} conflicted, and {3} erroneous items. ".format(len(addLists), len(removeLists), len(conflictLists), len(exceptionLists)))
		while True:
			choice = selectOperation(bool(addLists), bool(removeLists), bool(differLists))
			if choice == 1:
				doRemove(dir2, addLists)
			elif choice == 2:
				doCopy(dir2, dir1, addLists)
			elif choice == 3:
				doCopy(dir1, dir2, removeLists)
			elif choice == 4:
				doRemove(dir1, removeLists)				
			elif choice == 5:
				doCopy(dir1, dir2, differLists)
			elif choice == 6:
				doCopy(dir2, dir1, differLists)
			elif choice == 7:
				fpath = input("请输入比对结果保存路径（留空取消）：").replace("\"", "")
				if fpath:
					try:
						with open(fpath, "w", encoding = "utf-8") as f:
							f.write("Source = \"{0}\"\n".format(dir1))
							f.write("Target = \"{0}\"\n".format(dir2))
							f.write("addLists = {0}\n".format(addLists))
							f.write("removeLists = {0}\n".format(removeLists))
							f.write("conflictLists = {0}\n".format(conflictLists))
							f.write("exceptionLists = {0}\n".format(exceptionLists))
							if compareFileContent:
								f.write("differLists = {0}\n".format(differLists))
								f.write("Totally {0} added, {1} removed, and {2} different files. \n".format(len(addLists), len(removeLists), len(differLists)))
							else:
								f.write("Totally {0} added and {1} removed files. \n".format(len(addLists), len(removeLists)))
						print("保存成功！")
					except Exception as e:
						print("保存失败，异常信息如下：")
						print(e)
			elif choice == 8:
				return doCompare(dir1, dir2, compareFileContent = compareFileContent, caseSensitive = caseSensitive, state = state)
			elif choice == 9:
				try:
					return not any([addLists, removeLists, conflictLists, exceptionLists, differLists])
				except: # 未定义变量
					return None
			elif choice == 0:
				state[0] = False
				try:
					return not any([addLists, removeLists, conflictLists, exceptionLists, differLists])
				except: # 未定义变量
					return None

def main() -> int:
	state = [True]
	while state[0]:
		sourcePath = input("请输入源文件夹路径：").replace("\"", "")
		targetPath = input("请输入目标文件夹路径：").replace("\"", "")
		compareFileContent = input("请选择是否需要比较文件内容（输入“Y”表示“是”）：").upper() in ("1", "Y")
		caseSensitive = input("请选择大小写是否敏感（输入“Y”表示“是”）：").upper() in ("1", "Y")
		bRet = doCompare(sourcePath, targetPath, compareFileContent = compareFileContent, caseSensitive = caseSensitive, state = state)
		clearScreen()
	return EXIT_SUCCESS if bRet else EXIT_FAILURE



if __name__ == "__main__":
	exit(main())
```

PS：某些输出处貌似有点中英混搭，请多多谅解。

最后，附上一些运行截图：

![多层级进度条显示](https://i-blog.csdnimg.cn/blog_migrate/5e9bb539972b0c849a2c67484e7d6550.png)
![中断运行与后续操作](https://i-blog.csdnimg.cn/blog_migrate/a0728058d5cd4139eebb4be8ba254da5.png)
—— 2024 年 9 月 27 日更新以下内容 ——

适配了一下在大小写敏感的操作系统中人为关闭大小写敏感开关的同步，顺便用面向对象的格式重构了下代码。

欢迎在 GitHub 中访问，链接如下：[https://github.com/BatchClayderman/directoryComparator](https://github.com/BatchClayderman/directoryComparator)。

```
import os
from sys import exit
from shutil import copy, copytree, rmtree
from hashlib import new as newHash
from time import sleep, time
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)
PLATFORM = __import__("platform").system().upper()
CLEAR_SCREEN_COMMAND = ("CLS" if "WINDOWS" == PLATFORM else "clear") if __import__("sys").stdin.isatty() else None


# Classes #
class ProgressBar:
	def __init__(self:object, total:int, c:int = 0, desc:str = "", postfix:str = "", ncols:int = 100) -> object:
		self.__total = total if isinstance(total, int) and total >= 1 else 1
		self.__c = c if isinstance(c, int) and c >= 0 else 0
		self.__desc = str(desc)
		self.__postfix = str(postfix)
		self.__ncols = ncols if isinstance(ncols, int) and ncols >= 10 else 10
		self.__print()
	def update(self:object, c:int = 1) -> bool:
		if isinstance(c, int) and c >= 0:
			self.__c += c
			if self.__c > self.__total:
				self.__c = self.__total
				self.__print()
				return False
			else:
				self.__print()
				return True
		else:
			return False
	def set_postfix(self:object, postfix:str) -> None:
		self.__postfix = str(postfix)
	def __print(self:object) -> bool:
		print("\r" + " " * self.__ncols + "\r" + str(self)[:self.__ncols], end = "")
	def __str__(self:object) -> str:
		return "{0}: {1} / {2} = {3:.2f}% {4}".format(self.__desc, self.__c, self.__total, 100 * self.__c / self.__total, self.__postfix)

class UniqueList(list):
	def append(self:object, ele:object) -> bool:
		if ele in self:
			return False
		else:
			super().append(ele)
			return True

class Comparison:
	def __init__(self:object, ncols:int = 100) -> object:
		# Outer Parameters #
		self.__ncols = ncols if isinstance(ncols, int) and ncols >= 10 else 10
		self.__sourcePath = None
		self.__targetPath  = None
		self.__compareFileContent = None
		self.__caseSensitive = None
		self.__enableSoftLinks = False
		
		# Internal Parameters #
		self.__addingList = UniqueList()
		self.__removalList = UniqueList()
		self.__conflictList = UniqueList()
		self.__exceptionList = UniqueList()
		self.__differenceList = UniqueList()
		self.__specialFolders = ["", ".", ".."]
		self.__flag = 2 # 0 = E, 1 = R, 2 = N
	def __getRelPath(self:object, path:str, start:str) -> str: # avoid computing exceptions
		try:
			return os.path.relpath(path, start)
		except:
			return os.path.abspath(path)
	def __computeSHA256(self:object, fpath:str) -> str|Exception:
		try:
			with open(fpath, "rb") as f:
				hash = newHash("SHA256")
				for chunk in iter(lambda: f.read(1 << 20), b""):
					hash.update(chunk)
				return hash.hexdigest()
		except BaseException as e:
			return e
	def __consoleLayerUp(self:object) -> None:
		print("\r" + " " * self.__ncols + "\x1b[F\x1b[K", end = "", flush = True) # go up a layer
	def __consoleLayerDown(self:object) -> None:
		print(flush = True) # go down a layer
	def __compare(self:object, dir1:str, dir2:str, layer:int = 0) -> bool:
		# List Getting #
		try: # sort the items received from the OS API and exclude some special folders
			if self.__caseSensitive:
				listDir1, listDir2 = sorted([item for item in os.listdir(dir1) if item not in self.__specialFolders]), sorted([item for item in os.listdir(dir2) if item not in self.__specialFolders])
			else:
				listDir1 = sorted([item for item in os.listdir(dir1) if item not in self.__specialFolders], key = lambda x:x.upper())
				listDir2 = sorted([item for item in os.listdir(dir2) if item not in self.__specialFolders], key = lambda x:x.upper())
		except BaseException as e:
			self.__exceptionList.append((self.__getRelPath(dir1, self.__sourcePath), e))
			self.__consoleLayerUp()
			return False
		pBar = ProgressBar(total = len(listDir1) + len(listDir2), desc = "Layer {0}".format(layer), postfix = "(a, r, c, e, d) = (0, 0, 0, 0, 0)", ncols = self.__ncols)
		
		# Conflict Exclusion #
		assistDir1, assistDir2 = (listDir1[::], listDir2[::]) if self.__caseSensitive else ([item.upper() for item in listDir1], [item.upper() for item in listDir2]) # handle issues of repeated directories and the switch of case sensitivity
		setDir1 = set(assistDir1)
		if len(setDir1) != len(assistDir1):
			for ele in setDir1:
				if assistDir1.count(ele) > 1:
					while ele in assistDir1:
						idx = assistDir1.index(ele)
						self.__conflictList.append(self.__getRelPath(os.path.join(dir1, listDir1[idx]), self.__sourcePath))
						del assistDir1[idx], listDir1[idx]
						pBar.set_postfix("(a, r, c, e, d) = (0, 0, {0}, 0, 0)".format(len(self.__conflictList)))
						pBar.update(1)
					while ele in assistDir2:
						idx = assistDir2.index(ele)
						self.__conflictList.append(self.__getRelPath(os.path.join(dir2, listDir2[idx]), self.__targetPath))
						del assistDir2[idx], listDir2[idx]
						pBar.set_postfix("(a, r, c, e, d) = (0, 0, {0}, 0, 0)".format(len(self.__conflictList)))
						pBar.update(1)
		setDir2 = set(assistDir2)
		if len(setDir2) != len(assistDir2):
			for ele in setDir2:
				if assistDir2.count(ele) > 1:
					while ele in assistDir1:
						idx = assistDir1.index(ele)
						self.__conflictList.append(self.__getRelPath(os.path.join(dir1, listDir1[idx]), self.__sourcePath))
						del assistDir1[idx], listDir1[idx]
						pBar.set_postfix("(a, r, c, e, d) = (0, 0, {0}, 0, 0)".format(len(self.__conflictList)))
						pBar.update(1)
					while ele in assistDir2:
						idx = assistDir2.index(ele)
						self.__conflictList.append(self.__getRelPath(os.path.join(dir2, listDir2[idx]), self.__targetPath))
						del assistDir2[idx], listDir2[idx]
						pBar.set_postfix("(a, r, c, e, d) = (0, 0, {0}, 0, 0)".format(len(self.__conflictList)))
						pBar.update(1)
		
		# Comparison #
		try:
			while listDir1 and listDir2:
				if listDir1[0] == listDir2[0] or not self.__caseSensitive and listDir1[0].upper() == listDir2[0].upper(): # compare attributes if the two names are the same
					target1, target2 = os.path.join(dir1, listDir1[0]), os.path.join(dir2, listDir2[0])
					if os.path.islink(target1) and os.path.islink(target2): # both are soft links
						if self.__enableSoftLinks:
							theAbsolutePathsAreDifferent = False # no need to compare if conflicts exist
							try:
								link1, link2 = os.readlink(target1), os.readlink(target2)
								theAbsolutePathsAreDifferent = not (os.path.isabs(link1) and os.path.isabs(link2) and link1 == link2)
							except BaseException as e:
								self.__exceptionList.append((self.__getRelPath(target1, self.__sourcePath), e))
								self.__consoleLayerUp()
							if theAbsolutePathsAreDifferent:
								if os.path.isdir(target1) and os.path.isdir(target2): # do recursion if both are linked to folders
									self.__consoleLayerDown()
									try:
										self.__compare(target1, target2, layer = layer + 1)
									except BaseException as e:
										self.__exceptionList.append((self.__getRelPath(target1, self.__sourcePath), e))
										self.__consoleLayerUp()
								elif os.path.isfile(target1) and os.path.isfile(target2): # both are linked to files
									if self.__compareFileContent:
										sha1, sha2 = self.__computeSHA256(target1), self.__computeSHA256(target2)
										if isinstance(sha1, str) and isinstance(sha2, str):
											if sha1 != sha2:
												self.__differenceList.append(self.__getRelPath(target1, self.__sourcePath))
										else:
											self.__exceptionList.append((self.__getRelPath(target1, self.__sourcePath), (sha1, sha2)))
								else: # different attributes
									self.__conflictList.append(self.__getRelPath(target1, self.__sourcePath))
						elif self.__compareFileContent:
							try:
								if os.readlink(target1) != os.readlink(target2): # the positions they link to are the file content
									self.__differenceList.append(self.__getRelPath(target1, self.__sourcePath))
							except BaseException as e:
								self.__exceptionList.append((self.__getRelPath(target1, self.__sourcePath), e))
					elif os.path.isdir(target1) and os.path.isdir(target2): # do recursion if both are folders
						self.__consoleLayerDown()
						try:
							self.__compare(target1, target2, layer = layer + 1)
						except BaseException as e:
							self.__exceptionList.append((self.__getRelPath(target1, self.__sourcePath), e))
							self.__consoleLayerUp()
					elif os.path.isfile(target1) and os.path.isfile(target2): # both are files
						if self.__compareFileContent:
							sha1, sha2 = self.__computeSHA256(target1), self.__computeSHA256(target2)
							if isinstance(sha1, str) and isinstance(sha2, str):
								if sha1 != sha2:
									self.__differenceList.append(self.__getRelPath(target1, self.__sourcePath))
							else:
								self.__exceptionList.append((self.__getRelPath(target1, self.__sourcePath), (sha1, sha2)))
					else: # different attributes
						self.__conflictList.append(self.__getRelPath(target1, self.__sourcePath))
					listDir1.pop(0)
					listDir2.pop(0)
					pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(self.__addingList), len(self.__removalList), len(self.__conflictList), len(self.__exceptionList), len(self.__differenceList)))
					pBar.update(2)
				elif self.__caseSensitive and listDir1[0] < listDir2[0] or not self.__caseSensitive and listDir1[0].upper() < listDir2[0].upper(): # the first object is smaller
					self.__removalList.append(self.__getRelPath(os.path.join(dir1, listDir1[0]), self.__sourcePath)) # mark as removal
					listDir1.pop(0)
					pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(self.__addingList), len(self.__removalList), len(self.__conflictList), len(self.__exceptionList), len(self.__differenceList)))
					pBar.update(1)
				elif self.__caseSensitive and listDir1[0] > listDir2[0] or not self.__caseSensitive and listDir1[0].upper() > listDir2[0].upper(): # the second object is smaller
					self.__addingList.append(self.__getRelPath(os.path.join(dir2, listDir2[0]), self.__targetPath)) # mark as adding
					listDir2.pop(0)
					pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(self.__addingList), len(self.__removalList), len(self.__conflictList), len(self.__exceptionList), len(self.__differenceList)))
					pBar.update(1)
			if listDir1:
				self.__removalList.extend([self.__getRelPath(os.path.join(dir1, item), self.__sourcePath) for item in listDir1])
				pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(self.__addingList), len(self.__removalList), len(self.__conflictList), len(self.__exceptionList), len(self.__differenceList)))
				pBar.update(len(listDir1))
			elif listDir2:
				self.__addingList.extend([self.__getRelPath(os.path.join(dir2, item), self.__targetPath) for item in listDir2])
				pBar.set_postfix("(a, r, c, e, d) = ({0}, {1}, {2}, {3}, {4})".format(len(self.__addingList), len(self.__removalList), len(self.__conflictList), len(self.__exceptionList), len(self.__differenceList)))
				pBar.update(len(listDir2))
			self.__consoleLayerUp()
			return True
		except BaseException as e:
			self.__exceptionList.append((self.__getRelPath(dir1, self.__sourcePath), e))
			self.__exceptionList.append((self.__getRelPath(dir2, self.__targetPath), e))
			self.__consoleLayerUp()
			return False
	def __selectAnOperation(self:object, addingFlag:bool, removalFlag:bool, differenceFlag:bool) -> str:
		print("addingList = {0}".format(self.__addingList))
		print("removalList = {0}".format(self.__removalList))
		print("conflictList = {0}".format(self.__conflictList))
		print("exceptionList = {0}".format(self.__exceptionList))
		if self.__compareFileContent:
			print("differenceList = {0}".format(self.__differenceList))
			print(														\
				"Totally {0} added, {1} removed, {2} conflicted, {3} erroneous, and {4} different items. ".format(				\
					len(self.__addingList), len(self.__removalList), len(self.__conflictList), len(self.__exceptionList), len(self.__differenceList)	\
				)													\
			)
		else:
			print("Totally {0} added, {1} removed, {2} conflicted, and {3} erroneous items. ".format(len(self.__addingList), len(self.__removalList), len(self.__conflictList), len(self.__exceptionList)))
		print("\nNote: The removing operation means deleting objects directly instead of moving objects to the recycle bin. \nOperations provided are listed as follows. ")
		if addingFlag:
			print("\t1 = Remove the objects the target has but the source does not from the source (source -> target)")
			print("\t2 = Copy the objects the target has but the source does not from the target to the source (target -> source)")
		if removalFlag:
			print("\t3 = Copy the objects the source has but the target does not from the source to the target (source -> target)")
			print("\t4 = Remove the objects the source has but the target does not from the target (target -> source)")
		if differenceFlag:
			print("\t5 = Synchronize the different objects from the source to the target (source -> target)")
			print("\t6 = Synchronize the different objects from the target to the source (target -> source)")
		if addingFlag or removalFlag or differenceFlag:
			print("\tS = source -> target (135)")
			print("\tT = target -> source (246)")
		print("\tD = Dump the comparison results")
		print("\tR = Rescan again with the original configuration")
		print("\tN = Perform new scanning")
		print("\tE = Exit")
		print()
		try:
			sRet = input("Please select an operation to continue: ").upper()
		except:
			sRet = None
		availabilityList = (["1", "2"] if addingFlag else []) + (["3", "4"] if removalFlag else []) + (["5", "6"] if differenceFlag else []) + (["S", "T"] if addingFlag or removalFlag or differenceFlag else []) + ["D", "R", "N", "E"]
		while True:
			if sRet in availabilityList:
				if sRet in ("D", "R", "N", "E") or input("The program is about to execute Operation {0}. \nTo avoid accidental touch, please input \"Y\" before the program goes on: ".format(sRet)) == "Y":
					return sRet
				else:
					try:
						sRet = input("The operation is not confirmed by users. Please select again: ").upper()
					except:
						sRet = None
			else:
				try:
					sRet = input("The operation is invalid. Please select again: ").upper()
				except:
					sRet = None
	def __doRemoval(self:object, folder:str, taskList:list) -> bool:
		if not taskList:
			return False
		successIndexList, failureExceptionList, totalLength = [], [], len(taskList)
		self.__consoleLayerDown()
		pBar = ProgressBar(total = totalLength, desc = "Removing", postfix = "(s, f) = (0, 0)", ncols = self.__ncols)
		for i, item in enumerate(taskList):
			toRemoveFp = os.path.join(folder, item)
			try:
				if os.path.isdir(toRemoveFp):
					rmtree(toRemoveFp)
				else:
					os.remove(toRemoveFp)
				successIndexList.append(i)
			except BaseException as e:
				failureExceptionList.append((toRemoveFp, e))
			pBar.set_postfix = "(s, f) = ({0}, {1})".format(len(successIndexList), len(failureExceptionList))
			pBar.update(1)
		self.__consoleLayerUp()
		for idx in successIndexList[::-1]:
			taskList.pop(idx)
		if failureExceptionList:
			print("Details of the {0} failure(s): ".format(len(failureExceptionList)))
			for i, failureException in enumerate(failureExceptionList):
				print("[{0}] \"{1}\" -> {2}".format(i, failureException[0], failureException[1]))
		print("\rThe removing is finished with the success rate of {0} / {1} = {2}%. ".format(len(successIndexList), totalLength, 100 * len(successIndexList) / totalLength)) # The situation of "/0" should not exist
		return not bool(failureExceptionList)
	def __doCopying(self:object, dir1:str, dir2:str, taskList:list) -> bool:
		if not taskList:
			return False
		successIndexList, failureExceptionList, totalLength = [], [], len(taskList)
		self.__consoleLayerDown()
		pBar = ProgressBar(total = totalLength, desc = "Copying", postfix = "(s, f) = (0, 0)", ncols = self.__ncols)
		for i, item in enumerate(taskList):
			sourceFp = os.path.join(dir1, item)
			targetFp = os.path.join(dir2, item)
			try:
				if os.path.isdir(sourceFp):
					copytree(sourceFp, targetFp)
				else:
					copy(sourceFp, targetFp)
				successIndexList.append(i)
			except BaseException as e:
				failureExceptionList.append((sourceFp, targetFp, e))
		self.__consoleLayerUp()
		for idx in successIndexList[::-1]:
			taskList.pop(idx)
		if failureExceptionList:
			print("Details of the {0} failure(s): ".format(len(failureExceptionList)))
			for i, failureException in enumerate(failureExceptionList):
				print("[{0}] \"{1}\" -> \"{2}\" -> {3}".format(i, failureException[0], failureException[1], failureException[2]))
		print("\rThe copying is finished with the success rate of {0} / {1} = {2}%. ".format(len(successIndexList), totalLength, 100 * len(successIndexList) / totalLength)) # The situation of "/0" should not exist
		return not bool(failureExceptionList)
	def __convertTime(self:object, t:float) -> str:
		if isinstance(t, (float, int)):
			if t <= 0.000000001: # <= 1 ns
				return "{0:.3f} nanosecond".format(t * 1000000000)
			elif t <= 0.000001: # (1 ns, 1000 ns]
				return "{0:.3f} nanoseconds".format(t * 1000000000)
			elif t <= 0.001: # (1 us, 1000 us]
				return "{0:.3f} Microseconds".format(t * 1000000)
			elif t <= 1: # (1 ms, 1000 ms]
				return "{0:.3f} milliseconds".format(t * 1000)
			else: # > 1 s
				return "{0:.3f} seconds".format(t)
		else:
			return "unknown"
	def __doComparison(self:object) -> bool:
		clearScreen()
		print("Working directory: \"{0}\"".format(os.getcwd()))
		print("Source: \"{0}\"".format(self.__sourcePath))
		print("Target: \"{0}\"".format(self.__targetPath))
		print()
		if self.__sourcePath == self.__targetPath or not self.__caseSensitive and self.__sourcePath.upper() == self.__targetPath.upper():
			print("The source path and the target path are the same. ")
			pause()
			self.__flag = 2 # force users to input data again
			return False
		elif not os.path.isdir(self.__sourcePath) or not self.__enableSoftLinks and os.path.islink(self.__sourcePath):
			if not os.path.isdir(self.__targetPath) or not self.__enableSoftLinks and os.path.islink(self.__targetPath):
				print("Both the source path and the target path do not exist or neither of them are valid directories. ")
			else:
				print("The source path does not exist or is not a valid directory. ")
			pause()
			self.__flag = 2 # force users to input data again
			return False
		elif not os.path.isdir(self.__targetPath) or not self.__enableSoftLinks and os.path.islink(self.__targetPath):
			print("The target path does not exist or is not a valid directory. ")
			pause()
			self.__flag = 2 # force users to input data again
			return False
		else:
			self.__addingList.clear()
			self.__removalList.clear()
			self.__conflictList.clear()
			self.__exceptionList.clear()
			self.__differenceList.clear()
			startTime = time()
			try:
				self.__compare(self.__sourcePath, self.__targetPath)
			except BaseException as e:
				print("\nExceptions occurred. Details are as follows. \n{0}".format(e))
			endTime = time()
			print("\nNote: The time used is {0}. ".format(self.__convertTime(endTime - startTime)))
			while True:
				choice = self.__selectAnOperation(bool(self.__addingList), bool(self.__removalList), bool(self.__differenceList))
				print()
				if "1" == choice:
					self.__doRemoval(self.__targetPath, self.__addingList)
				elif "2" == choice:
					self.__doCopying(self.__targetPath, self.__sourcePath, self.__addingList)
				elif "3" == choice:
					self.__doCopying(self.__sourcePath, self.__targetPath, self.__removalList)
				elif "4" == choice:
					self.__doRemoval(self.__sourcePath, self.__removalList)
				elif "5" == choice:
					self.__doCopying(self.__sourcePath, self.__targetPath, self.__differenceList)
				elif "6" == choice:
					self.__doCopying(self.__targetPath, self.__sourcePath, self.__differenceList)
				elif "S" == choice:
					if self.__addingList:
						self.__doRemoval(self.__targetPath, self.__addingList)
					if self.__removalList:
						self.__doCopying(self.__sourcePath, self.__targetPath, self.__removalList)
					if self.__differenceList:
						self.__doCopying(self.__sourcePath, self.__targetPath, self.__differenceList)
				elif "T" == choice:
					if self.__addingList:
						self.__doCopying(self.__targetPath, self.__sourcePath, self.__addingList)
					if self.__removalList:
						self.__doRemoval(self.__sourcePath, self.__removalList)
					if self.__differenceList:
						self.__doCopying(self.__targetPath, self.__sourcePath, self.__differenceList)
				elif "D" == choice:
					try:
						fpath = input("Please input the path for saving the results: ").replace("\"", "")
					except: # KeyboardInterrupt
						fpath = None
					if fpath:
						try:
							with open(fpath, "w", encoding = "utf-8") as f:
								f.write("Source = \"{0}\"\n".format(self.__sourcePath))
								f.write("Target = \"{0}\"\n".format(self.__targetPath))
								f.write("addingList = {0}\n".format(self.__addingList))
								f.write("removalList = {0}\n".format(self.__removalList))
								f.write("conflictList = {0}\n".format(self.__conflictList))
								f.write("exceptionList = {0}\n".format(self.__exceptionList))
								if self.__compareFileContent:
									f.write("differenceList = {0}\n".format(self.__differenceList))
									f.write("Totally {0} added, {1} removed, and {2} different files. \n".format(len(self.__addingList), len(self.__removalList), len(self.__differenceList)))
								else:
									f.write("Totally {0} added and {1} removed files. \n".format(len(self.__addingList), len(self.__removalList)))
							print("Successfully save to \"{0}\". ".format(fpath))
						except BaseException as e:
							print("Failed saving to \"{0}\". Details are as follows. \n{1}".format(fpath, e))
				elif "R" == choice:
					self.__flag = 1
					return not any([self.__addingList, self.__removalList, self.__conflictList, self.__exceptionList, self.__differenceList])
				elif "N" == choice:
					self.__flag = 2
					return not any([self.__addingList, self.__removalList, self.__conflictList, self.__exceptionList, self.__differenceList])
				elif "E" == choice:
					self.__flag = 0
					return not any([self.__addingList, self.__removalList, self.__conflictList, self.__exceptionList, self.__differenceList])
				print()
				pause()
				clearScreen() # new operation selection
				print("Source: \"{0}\"".format(self.__sourcePath))
				print("Target: \"{0}\"".format(self.__targetPath))
				print("\nNote: The incremental update of the comparison results is performed. " if choice in ("1", "2", "3", "4", "5", "6", "S", "T") else "")
	def interact(self:object) -> bool:
		bRet = False
		while self.__flag:
			clearScreen()
			if self.__flag > 1 or self.__sourcePath is None and self.__targetPath is None and self.__compareFileContent is None and self.__caseSensitive is None:
				try:
					print("Note: Please press \"Ctrl + C\" to enter the data again if wrong data are accidentally input. \nWorking directory: \"{0}\"".format(os.getcwd()))
					self.__sourcePath = input("Please input the source path (leave it blank to exit): ").replace("\"", "")
					if ""  == self.__sourcePath:
						break
					self.__targetPath = input("Please input the target path (leave it blank to exit): ").replace("\"", "")
					if ""  == self.__targetPath:
						break
					self.__compareFileContent = input("Please answer whether the file contents should be compared [yN]: ").upper() in ("1", "T", "TRUE", "Y", "YES")
					print("The current operating system {0} case sensitive. ".format("is not" if "WINDOWS" == PLATFORM else "is"))
					self.__caseSensitive = input("Please answer whether it should be case sensitive [yN]: ").upper() in ("1", "T", "TRUE", "Y", "YES")
					if "WINDOWS" == PLATFORM:
						self.__enableSoftLinks = False
					else:
						print("The current operating system supports soft links. Please use \"Ctrl + C\" if infinite recursion occurs. ")
						self.__enableSoftLinks = input("Please answer whether soft links should be enabled [yN]: ").upper() in ("1", "T", "TRUE", "Y", "YES")
				except: # KeyboardInterrupt
					self.__sourcePath, self.__targetPath, self.__compareFileContent, self.__caseSensitive, self.__enableSoftLinks = None, None, None, None, False
					continue
			try:
				bRet = self.__doComparison()
			except BaseException as e:
				if isinstance(e, KeyboardInterrupt):
					print("\nThe comparison algorithm is interrupted by users. ")
				else:
					print("\nUnexpected exceptions occurred while performing the comparison algorithm. Details are as follows. \n{0}".format(e))
				pause()
		clearScreen()
		return bRet


# Main Functions #
def clearScreen(fakeClear:int = 120) -> bool:
	if CLEAR_SCREEN_COMMAND is not None and not os.system(CLEAR_SCREEN_COMMAND):
		return True
	else:
		try:
			print("\n" * int(fakeClear))
		except:
			print("\n" * 120)
		return False

def preExit(countdownTime:int = 5) -> None:
	clearScreen()
	try:
		cntTime = int(countdownTime)
		length = len(str(cntTime))
	except:
		print("Program ended. ")
		clearScreen()
		return
	while cntTime > 0:
		print("\rProgram ended, exiting in {{0:>{0}}} second(s). ".format(length).format(cntTime), end = "")
		try:
			sleep(1)
		except:
			cntTime = 0
			break
		cntTime -= 1
	print("\rProgram ended, exiting in {{0:>{0}}} second(s). ".format(length).format(cntTime))
	clearScreen()

def pause() -> None:
	print("Please press the enter key to continue. ")
	try:
		input()
	except:
		pass

def main() -> int:
	try:
		comparison = Comparison()
		bRet = comparison.interact()
		preExit()
		return EXIT_SUCCESS if bRet else EXIT_FAILURE
	except BaseException as e:
		try:
			print("The program is interrupted by users. " if isinstance(e, KeyboardInterrupt) else "Unexpected exceptions occurred in the main function. Details are as follows. \n{0}".format(e))
			preExit()
		except:
			pass
		finally:
			return EOF



if __name__ == "__main__":
	exit(main())
```
