为了使得程序更具有鲁棒性，在即将打开并写入一个文件（file）时，我们通常需要检测这个文件的父文件夹（folder）是否存在，如果不存在，则需要创建目录（directory）。例如，当我们希望写出数据到 ``C:\1\2\3.txt`` 中但父文件夹 ``2``（即目录 ``C:\1\2``）不存在时，就需要一段代码去创建这个目录。如果使用 Python，下面的代码可能就能处理这个目录。

```
import os

def handleFolder(fd:str) -> bool:
	folder = str(fd)
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
```

这段代码首先检查传递的父目录路径是否为空，如果为空则说明是文件使用的是一个相对路径且其父文件夹为当前文件夹。一般而言，在没有使用驱动级删除目录的情况下，如果当前程序能成功将某个目录路径设置成了工作目录路径，那么这个目录一般是存在的且在程序退出或切换工作目录到其它目录前这个目录都是存在的。因此，不需要考虑当前文件夹是否存在，直接返回 ``True``。如果目录路径不为空，则可以直接使用 ``os.path.exists`` 判断目标目录路径是否存在。如果存在，则判断是否为目录路径上的对象（object）是否为一个文件夹即可。即使不是，我们也没有办法做什么，直接返回 ``False``~~，毕竟总不能把别人的文件或者软连接（soft link）删掉吧~~！如果不存在，则直接使用 ``os.makedirs`` 创建（这会自动完成递归创建如果父父文件夹也不存在）。注意吃掉异常，必要时可以提示异常的内容。

在 C/C++ 上，上述思路还是可行的。然而，C/C++ 没有 Python 的代码这么精炼，还需考虑多一些情况。无论是在内核驱动还是在应用层面，Windows 的应用程序编程接口（Application Programming Interface，简称 API）都十分强大。现先以 RTree 类为例，给出一段有关写入 rTreeFilePath 前目录预处理的可能的代码：

```
#include<iostream>
#include <iostream>
#if defined WIN32 || defined _WIN32 || defined _WIN64
#include <windows.h>
#endif
/* ... */
using namespace std;
/* ... */
class RTree
{
private:
	string rTreeFilePath{};
	/* ... */
#if defined WIN32 || defined _WIN32 || defined _WIN64
	bool handleFolder(const bool tryToCreate) const
	{
		/* File */
		string dirPath = this->rTreeFilePath;
		replace(dirPath.begin(), dirPath.end(), '/', '\\'); // uniform the path separator
		const string::size_type pos = dirPath.find_last_of("\\");
		if (string::npos == pos) // the output file path is located in the current working folder since this is a relative path without any path separators
			return true; // to exclude the current working folder
		else if (string::npos != dirPath.find("\\\\"))
		{
			cout << "Failed to write the results to \"" << this->rTreeFilePath << "\" since the path is invalid. " << endl;
			return false;
		}
		
		/* Folder */
		dirPath = dirPath.substr(0, pos); // to aoivd paths like "C:\\1.txt\\3.txt" ("C:\\1.txt\\" will be reported as a invalid object instead of a file)
		if ("" == dirPath) // to exclude the root folder of this program ("\\")
			return true;
		else
		{
			if (dirPath.size() >= 2 && ':' == dirPath[dirPath.size() - 1]) // to avoid paths like "C:" since "C:" is different from "C:\\"
				dirPath += '\\';
			const DWORD dWord = GetFileAttributesA(dirPath.c_str());
			if (INVALID_FILE_ATTRIBUTES == dWord)
			{
				const DWORD lastError = GetLastError();
				if (ERROR_PATH_NOT_FOUND == lastError || ERROR_FILE_NOT_FOUND == lastError) // really not exist
					if (tryToCreate)
					{
						/* create parent folders level by level */
						stringstream ss(dirPath);
						string fullLevel{};
						getline(ss, fullLevel, '\\'); // remove the initial '\\'
						CreateDirectoryA(fullLevel.c_str(), NULL);
						while (!ss.eof())
						{
							string currentLevel{};
							getline(ss, currentLevel, '\\');
							fullLevel += "\\" + currentLevel;
							CreateDirectoryA(fullLevel.c_str(), NULL);
						}
						return this->handleFolder(false); // do not try to create again
					}
					else
					{
						cout << "Failed to write the results to \"" << this->rTreeFilePath << "\" since the parent folder is not created successfully. " << endl;
						return false;
					}
				else
				{
					cout << "Failed to write the results to \"" << this->rTreeFilePath << "\" since an invalid path is specified (" << lastError << "). " << endl;
					return false;
				}
			}
			else if (dWord & FILE_ATTRIBUTE_DIRECTORY) // the folder already exists
				return true;
			else // a non-folder object having the same name with the folder exists
			{
				cout << "Failed to write the results to \"" << this->rTreeFilePath << "\" since a non-folder object having the same name as the parent folder exists. " << endl;
				return false;
			}
		}
	}
	bool handleFolder() const { return this->handleFolder(true); }
#endif
	/* ... */
	
public:
	/* ... */
	bool writeResults()
	{
#if defined WIN32 || defined _WIN32 || defined _WIN64
		if (!this->handleFolder())
			return false;
#endif
		/* ... */
	}
	/* ... */
};
/* ... */
```

改动在于：
- 需要考虑对不同操作系统的兼容，此处使用 WinAPI 可利用指示 Windows 平台的宏控制。
- 切割出父文件夹的目录路径前可能需要统一一下路径分隔符，如果没有路径分隔符号要知道是当前工作目录而不是强行切割导致可能的越界，Python 的 ``os.path.split`` 应该做了这个事情。
- 处理路径分隔符连续的情况（Java 做了这方面的处理）。
- 注意判断是否为磁盘根目录，如果是磁盘根目录，则需要加上一个路径分隔符号。这是因为 ``C:`` 和 ``C:\`` 是不一样的，前者指在驱动器 ``C:`` 上的之前用过的工作目录（没有就是根目录），后者指的是驱动器 ``C:`` 的根目录。本文所需要解决的问题中，目标文件若以 ``C:\1.txt`` 的形式存在，则目标文件一定是位于 C 盘根目录下，即应当将 ``C:\`` 传递给 Windows API。
- 在上一条中有的读者可能会疑惑为什么不直接统一保留最后的路径分隔符，这是因为如果目标文件 ``C:\1.txt\2.txt`` 的父文件夹 ``C:\1.txt`` 以文件的形式存在，用 WinAPI 获取 ``C:\1.txt`` 的属性会返回存在且为该路径导向的是一个文件，而用 WinAPI 获取 ``C:\1.txt\`` 的属性则会返回路径不合法，这样我们就无法给用户提供正确的对象冲突信息。
- 可以使用位运算直接判断对象是否为目录，有兴趣者可以直接查看宏定义。
- 需要递归建文件夹（代码实现上是递推），此处建议直接建完了再判断一次文件夹是否存在。如果遇到路径中出现了驱动器（无论是否存在都会返回拒绝访问）或者出现了类似于 ``../../../`` 的情况，每次创建都判断会很麻烦，所以建议直接递归处理完再调用本函数判断一次（函数最多再被调用 1 次）。

以下是两个可能的效果图，以管理员身份启动 cmd 后，执行了 ``@echo off & cls``（原谅我不想显示 ``indexing.exe`` 具体所在路径）。开始，``C:\`` 下无 ``3.txt`` 文件夹。随后执行 ``indexing.exe /rTree C:\3.txt/4/5/7.txt``，程序能正常递归创建文件夹。随后将 ``C:\3.txt`` 文件夹删除，在 ``C:\`` 下创建一个 ``3.txt`` 文件，再次执行该命令，程序报冲突，功能实现成功。
![效果](https://i-blog.csdnimg.cn/direct/a2dd353fd76e4c7a8a927f3fd96221c1.png)
![效果](https://i-blog.csdnimg.cn/direct/62a750643ba34f47a8b3d6d590746a10.png)

当然，以上实现都是初步的，如果去尝试写入文件 ``C:\..\..\1.txt``，不知道会发生什么。在未来，大概会提供两种选择，一是将根目录的 ``..`` 视为 ``.``，二是对根目录使用 ``..`` 时报异常。以后有时间再分享。
