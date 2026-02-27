最近有朋友让我批量去除一个文件夹中所有mp3音频的前6.2秒广告，查阅了CSDN，对以下链接的代码进行了一些优化，将优化后的代码放置于此。

> https://blog.csdn.net/weixin_40901505/article/details/135687886

Python 第三方库部署：

```
pip install pydub
```

Windows 安装 ffmpeg 的教程如下。

> https://www.geeksforgeeks.org/how-to-install-ffmpeg-on-windows/

另外，还发现了一个有用的网站，链接如下。

> https://kwm.worthsee.com/

完整代码如下：
```
import os
from multiprocessing import Pool
from pydub import AudioSegment
os.chdir(os.path.abspath(os.path.dirname(__file__)))
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
inputFolderPath = "data"
outputFolderPath = "converted"
musicFileExts = [".mp3"]
cutStart = 6200
cutEnd = None


def handleFolder(folder:str) -> bool:
	if folder in ("", ".", "./", ".\\"):
		return True
	elif os.path.exists(folder):
		return os.path.isdir(folder)
	else:
		try:
			os.makedirs(folder)
			return True
		except:
			return False

def worker(filename:str) -> bool:
	inputFp = os.path.join(inputFolderPath, filename)
	outputFp = os.path.join(outputFolderPath, filename)
	try:
		inputMusic = AudioSegment.from_mp3(inputFp)
		outputMusic = inputMusic[cutStart:cutEnd]
		if not handleFolder(os.path.split(outputFp)[0]):
			print("[X] \"{0}\" -> \"{1}\": The parent folder is not created successfully. ".format(inputFp, outputFp, e))
			return False
		outputMusic.export(outputFp, bitrate = "64k")
		print("[V] \"{0}\" -> \"{1}\". ".format(inputFp, outputFp))
		return True
	except Exception as e:
		print("[X] \"{0}\" -> \"{1}\": {2}. ".format(inputFp, outputFp, e))
		return False

def main() -> int:
	convertList = []
	for filename in os.listdir(inputFolderPath):
		if os.path.splitext(filename)[1].lower() in musicFileExts and os.path.isfile(os.path.join(inputFolderPath, filename)):
			convertList.append(filename)
	print("The following {0} item(s) will be converted. \n{1}".format(len(convertList), convertList))
	p = Pool(processes = min(len(convertList), os.cpu_count()))
	bRet = p.map(worker, convertList)
	print(bRet)
	return EXIT_SUCCESS if all(bRet) else EXIT_FAILURE



if __name__ == "__main__":
	exit(main())
```

运行截图：
![运行截图（1）](https://i-blog.csdnimg.cn/blog_migrate/f0d25ed1457d5adee865f16a494b2d62.png)
![运行截图2](https://i-blog.csdnimg.cn/blog_migrate/fc11ce7b0a5d557d467383479a65bbdb.png)

