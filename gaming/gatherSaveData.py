import os
from sys import exit
from shutil import copytree, rmtree
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
except:
	pass
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)


class Gatherer:
	def __init__(												\
		self:object, 											\
		sourcePaths:tuple = (										\
			os.path.join(os.getenv("USERPROFILE"), "AppData", "Roaming", "Rovio"), 			\
			os.path.join(os.getenv("USERPROFILE"), "AppData", "Roaming", "Goldberg SteamEmu Saves")	\
		), 												\
		targetFolderPath:str = "saveData", 								\
		defaultOverwrite:bool = False									\
	) -> object:
		self.__sourcePaths = tuple(sourcePath for sourcePath in sourcePaths if isinstance(sourcePath, str))
		self.__targetFolderPath = targetFolderPath if isinstance(targetFolderPath, str) else "saveData"
		self.__defaultOverwrite = defaultOverwrite if isinstance(defaultOverwrite, bool) else False
	def __handleFolder(self:object, fd:str) -> bool:
		try:
			folder = str(fd)
		except:
			return False
		if not folder:
			return True
		elif os.path.exists(folder):
			return os.path.isdir(folder)
		else:
			try:
				os.makedirs(folder)
				return True
			except:
				return False
	def __ask(self:object, path:str) -> bool:
		try:
			str(path)
		except:
			return False
		if self.__defaultOverwrite:
			return True
		else:
			try:
				choice = input("The path \"{0}\" already exists. Would you like to overwrite? [yN]".format(path))
			except:
				return False
			return choice.upper() in ("Y", "YES", "1", "T", "TRUE")
	def __remove(self:object, path:str) -> bool:
		try:
			str(path)
		except:
			return False
		if self.__ask(path):
			if os.path.isdir(path):
				try:
					rmtree(path)
					print("Successfully removed the directory \"{0}\". ".format(path))
					return True
				except BaseException as e:
					print("Failed to remove the directory \"{0}\". Exceptions are as follows. \n\t{1}".format(path, e))
					return False
			elif os.path.isfile(path):
				try:
					os.remove(path)
					print("Successfully removed the file \"{0}\". ".format(path))
					return True
				except BaseException as e:
					print("Failed to remove the file \"{0}\". Exceptions are as follows. \n\t{1}".format(path, e))
					return False
			else:
				print("Failed to remove the object \"{0}\" since it is neither a regular directory nor a regular file. ".format(path))
				return False
		else:
			print("Gathering for \"{0}\" will be skipped. ".format(path))
			return False
	def gather(self:object) -> tuple:
		successCount, totalCount = 0, 0
		if not self.__handleFolder(self.__targetFolderPath):
			print("Failed to initialize the target folder \"{0}\". ".format(self.__targetFolderPath))
			return (successCount, totalCount)
		for sourcePath in self.__sourcePaths:
			totalCount += 1
			if os.path.isdir(sourcePath):
				name = os.path.split(sourcePath)[1]
				targetPath = os.path.join(self.__targetFolderPath, name)
				if not os.path.exists(targetPath) or self.__remove(targetPath):
					try:
						copytree(sourcePath, targetPath)
						print("Successfully gathered \"{0}\" as a directory. ".format(targetPath))
						successCount += 1
					except BaseException as e:
						print("Failed to gather \"{0}\" as a directory. ".format(targetPath))
			elif os.path.isfile(sourcePath):
				name = os.path.split(sourcePath)[1]
				targetPath = os.path.join(self.__targetFolderPath, name)
				if not os.path.exists(targetPath) or self.__remove(targetPath):
					try:
						os.copy(sourcePath, os.path.join(targetPath, sourceName))
						print("Successfully gathered \"{0}\" as a file. ".format(targetPath))
						successCount += 1
					except BaseException as e:
						print("Failed to gather \"{0}\" as a file. ".format(targetPath))
			else:
				print("Failed to gather \"{0}\" since it is neither a regular directory nor a regular file. ".format(targetPath))
		return (successCount, totalCount)


def main() -> int:
	gatherer = Gatherer()
	successCount, totalCount = gatherer.gather()
	if totalCount:
		print("Successfully gathered {0} / {1} = {2:.2f}% objects. ".format(successCount, totalCount, successCount * 100 / totalCount))
		errorLevel = EXIT_SUCCESS if successCount == totalCount else EXIT_FAILURE
	else:
		print("Nothing was gathered. Please check whether your save data exist in the specified paths. ")
		errorLevel = EOF
	try:
		print("Please press the enter key to exit ({0}). ".format(errorLevel))
		input()
	except:
		print()
	exit(errorLevel)



if "__main__" == __name__:
	exit(main())