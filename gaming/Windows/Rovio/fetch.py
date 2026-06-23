import os
from urllib.parse import urljoin
from time import sleep
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
except:
	pass
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)


class InternetArchiveDownloader:
	def __init__(self:object, remoteUrl:str = "https://archive.org/download/angry-birds-pc/", localDirectory:str = ".", cacheFilePath:str = "./Content.html", forceUpdating:bool = True, skipExistingFiles:bool = True, maximumAttempts:int = 3, gapTime:int = 1) -> object:
		self.__remoteUrl = remoteUrl if isinstance(remoteUrl, str) else "https://archive.org/download/angry-birds-pc/"
		self.__localDirectory = localDirectory if isinstance(localDirectory, str) else "."
		self.__cacheFilePath = cacheFilePath if isinstance(cacheFilePath, str) else "./Content.html"
		self.__forceUpdating = forceUpdating if isinstance(forceUpdating, bool) else False
		self.__skipExistingFiles = skipExistingFiles if isinstance(skipExistingFiles, bool) else True
		self.__maximumAttempts = maximumAttempts if isinstance(maximumAttempts, int) and maximumAttempts >= 1 else 3
		self.__gapTime = gapTime if isinstance(gapTime, (float, int)) and gapTime > 0 else 1
		self.__items = []
	def initialize(self:object) -> bool:
		try:
			self.__session = __import__("requests").Session()
			self.__session.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
		except BaseException as e:
			print("Failed to initialize the HTTP session. Please check to make sure that ``from requests import Session`` can work correctly. ")
			return False
		try:
			os.makedirs(self.__localDirectory, exist_ok = True)
		except BaseException as e:
			print("Failed to initialize the local directory \"{0}\". ".format(self.__localDirectory))
			return False
		return True
	def parseHTML(self:object) -> int:
		# HTML Fetching #
		if self.__forceUpdating or not os.path.isfile(self.__cacheFilePath):
			try:
				response = self.__session.get(self.__remoteUrl)
				if response.status_code != 200:
					print("Failed to fetch HTML content with the status code {0}. ".format(response.status_code))
					return EOF
				content = response.content
				with open(self.__cacheFilePath, "wb") as f:
					f.write(content)
				del response
			except BaseException as e:
				print("Failed to save the HTML content from \"{0}\" to \"{1}\". Details are as follows. \n\t{2}".format(self.__remoteUrl, self.__cacheFilePath, e))
				return EOF
		else:
			try:
				with open(self.__cacheFilePath, "rb") as f:
					content = f.read()
			except BaseException as e:
				print("Failed to read the cached HTML content from \"{0}\". Details are as follows. \n\t{1}".format(self.__cacheFilePath, e))
				return EOF
		
		# Content Parsing #
		try:
			soup = __import__("bs4").BeautifulSoup(content, "html.parser")
			table = soup.find("table", class_ = "directory-listing-table")
		except:
			print("Failed to parse the HTML content. Please check to make sure that ``from bs4 import BeautifulSoup`` can work correctly. ")
			return None
		captionIndex, captionName, captionURL, captionSize = "Index", "Name", "URL", "Size"
		index, maximumNameLength, maximumURLLength, maximumSizeLength = 1, len(captionName), len(captionURL), len(captionSize)
		if table:
			rows = table.find_all("tr")[1:] # Skip headers and the parent menu
			for row in rows:
				cols = row.find_all("td")
				if len(cols) >= 3:
					linkTag = cols[0].find("a")
					if linkTag and linkTag.has_attr("href"):
						name, URL, size = linkTag.text.strip(), linkTag["href"], cols[2].text.strip()
						self.__items.append({"index":index, "name":name, "URL":URL, "size":size})
						index += 1
						maximumNameLength = max(maximumNameLength, len(name))
						maximumURLLength = max(maximumURLLength, len(URL))
						maximumSizeLength = max(maximumSizeLength, len(size))
		print("Successfully fetch {0} item(s) from \"{1}\". \n".format(len(self.__items), self.__remoteUrl))
		maximumIndexLength = max(len(captionIndex), len(str(index)))
		print("{0}\t{1}\t{2}\t{3}".format("-" * maximumIndexLength, "-" * maximumNameLength, "-" * maximumURLLength, "-" * maximumSizeLength))
		print("{{0:^{0}}}\t{{1:^{1}}}\t{{2:^{2}}}\t{{3:^{3}}}".format(maximumIndexLength, maximumNameLength, maximumURLLength, maximumSizeLength).format(captionIndex, captionName, captionURL, captionSize))
		print("{0}\t{1}\t{2}\t{3}".format("-" * maximumIndexLength, "-" * maximumNameLength, "-" * maximumURLLength, "-" * maximumSizeLength))
		for idx, item in enumerate(self.__items):
			print("{{0:^{0}}}\t{{1:^{1}}}\t{{2:^{2}}}\t{{3:^{3}}}".format(maximumIndexLength, maximumNameLength, maximumURLLength, maximumSizeLength).format(idx, item["name"], item["URL"], item["size"]))
		print("{0}\t{1}\t{2}\t{3}".format("-" * maximumIndexLength, "-" * maximumNameLength, "-" * maximumURLLength, "-" * maximumSizeLength))
		print()
		return len(self.__items)
	def __download(self:object, item:dict) -> bool:
		maximumIndexLength = len(str(len(self.__items)))
		index = item["index"]
		sourceURL = item["URL"]
		if not sourceURL.startswith(('http://', 'https://')):
			sourceURL = urljoin(self.__remoteUrl, sourceURL)
		targetPath = os.path.join(self.__localDirectory, item["name"])
		if self.__skipExistingFiles and os.path.isfile(targetPath):
			print("[{{0:>{0}}}] \"{{1}}\" -> \"{{2}}\" -> Skipped".format(maximumIndexLength).format(index, sourceURL, targetPath))
			return True
		else:
			attempt = 1
			while True:
				maximumPrintLength = 0
				try:
					response = self.__session.get(sourceURL, stream = True)
					response.raise_for_status()
					totalFileSize = int(response.headers.get("content-length", 0))
					toPrint = "[{{0:>{0}}}] \"{{1}}\" -> \"{{2}}\" -> 0 / {{3}} bytes".format(maximumIndexLength).format(index, sourceURL, targetPath, totalFileSize)
					toPrintLength = len(toPrint)
					maximumPrintLength = max(toPrintLength, maximumPrintLength)
					print(toPrint + " " * (maximumPrintLength - toPrintLength), end = "")
					with open(targetPath, "wb") as f:
						downloadedSize = 0
						for chunk in response.iter_content(chunk_size = 8192):
							if chunk:
								f.write(chunk)
								downloadedSize += len(chunk)
								if totalFileSize > 0:
									toPrint = "[{{0:>{0}}}] \"{{1}}\" -> \"{{2}}\" -> {{3}} / {{4}} bytes ({{5:.2f}}%)".format(maximumIndexLength).format(index, sourceURL, targetPath, downloadedSize, totalFileSize, downloadedSize * 100 / totalFileSize)
								else:
									toPrint = "[{{0:>{0}}}] \"{{1}}\" -> \"{{2}}\" -> {{3}} bytes downloaded".format(maximumIndexLength).format(index, sourceURL, targetPath, downloadedSize)
								toPrintLength = len(toPrint)
								maximumPrintLength = max(toPrintLength, maximumPrintLength)
								print("\r" + toPrint + " " * (maximumPrintLength - toPrintLength), end = "")
					print()
					return True
				except BaseException as e:
					if attempt < self.__maximumAttempts:
						toPrint = "[{{0:>{0}}}] \"{{1}}\" -> \"{{2}}\" -> {{3}} -> {{4}} / {{5}} attempt(s) used".format(maximumIndexLength).format(index, sourceURL, targetPath, e, attempt, self.__maximumAttempts)
						toPrintLength = len(toPrint)
						maximumPrintLength = max(toPrintLength, maximumPrintLength)
						print("\r" + toPrint + " " * (maximumPrintLength - toPrintLength))
						attempt += 1
						sleep(self.__gapTime)
					else:
						toPrint = "[{{0:>{0}}}] \"{{1}}\" -> \"{{2}}\" -> {{3}} -> Failed".format(maximumIndexLength).format(index, sourceURL, targetPath, e)
						toPrintLength = len(toPrint)
						maximumPrintLength = max(toPrintLength, maximumPrintLength)
						print("\r" + toPrint + " " * (maximumPrintLength - toPrintLength))
						break
			return False
	def downloadAll(self:object) -> int:
		successCount = 0
		for item in self.__items:
			if self.__download(item):
				successCount += 1
				sleep(self.__gapTime)
		print("\nSuccessfully downloaded {0} / {1} item(s). \n".format(successCount, len(self.__items)))
		return successCount

def main():
	# Parameters #
	remoteUrl = "https://archive.org/download/angry-birds-pc/"
	localDirectory = "."
	
	# Execution #
	downloader = InternetArchiveDownloader(remoteUrl, localDirectory)
	if not downloader.initialize():
		errorLevel = EOF
	else:
		totalCount = downloader.parseHTML()
		errorLevel = EXIT_SUCCESS if totalCount >= 1 and downloader.downloadAll() == totalCount else EXIT_FAILURE
	
	# Exit #
	try:
		print("Please press the enter key to exit ({0}). ".format(errorLevel))
		input()
	except:
		print()
	return errorLevel



if __name__ == "__main__":
	exit(main())