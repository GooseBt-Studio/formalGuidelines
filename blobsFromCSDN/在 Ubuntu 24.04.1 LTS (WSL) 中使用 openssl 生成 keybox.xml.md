看到“生成 keybox.xml”，大概率都会联想到 PIF 和 Tricky Store。这里就不多解释它们的用途了。最近在网上看到生成非 AOSP keybox 的教程，在这里做一些补充，并将代码打包成一个 Python 脚本。

参考自：
1) Idea 提供者：[https://xdaforums.com/t/tee-hacking.4662185/page-21#post-89847987](https://xdaforums.com/t/tee-hacking.4662185/page-21#post-89847987)~~（如果打不开或者被重定向去另一个网页可能要刷新几遍才能正确打开这个网页）~~ ，该原始 Idea 需要借助一个密码学工具网站；
2) RSA 私钥转换：[https://stackoverflow.com/questions/17733536/how-to-convert-a-private-key-to-an-rsa-private-key](https://stackoverflow.com/questions/17733536/how-to-convert-a-private-key-to-an-rsa-private-key)。

做出以下调整：
1) 直接使用一站式脚本执行，自动利用 openssl 生成三个 PEM 文件，如果用于预检测的 ``openssl version`` 命令执行失败，自动尝试通过 ``sudo apt-get install libssl-dev`` 进行安装；
2) 实现对新版 openssl 生成的 RSA 私钥进行识别，并从 PKCS8 转换为 PKCS1。

直接上 Python 代码，记得以 LF 形式保存换行符，并在 Ubuntu 24.04.1 LTS 中运行。
```
import os
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
except:
	pass
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)
keyboxFormatter = """<?xml version="1.0"?>
<AndroidAttestation>
<NumberOfKeyboxes>1</NumberOfKeyboxes>
<Keybox DeviceID="YourDeviceID">
<Key algorithm="ecdsa">
<PrivateKey format="pem">
{0}</PrivateKey>
<CertificateChain>
<NumberOfCertificates>1</NumberOfCertificates>
<Certificate format="pem">
{1}</Certificate>
</CertificateChain>
</Key>
<Key algorithm="rsa">
<PrivateKey format="pem">
{2}</PrivateKey>
</Key>
</Keybox>
</AndroidAttestation>"""


def execute(commandline:str) -> int|None:
	if isinstance(commandline, str):
		print("$ " + commandline)
		return os.system(commandline)
	else:
		return None

def handleOpenSSL(flag:bool = True) -> bool|None:
	if isinstance(flag, bool):
		errorLevel = execute("openssl version")
		if EXIT_SUCCESS == errorLevel:
			return True
		elif flag: # can try again
			execute("sudo apt-get install openssl libssl-dev")
			return handleOpenSSL(False)
		else:
			return False
	else:
		return None

def pressTheEnterKeyToExit(errorLevel:int|None = None):
	try:
		print("Please press the enter key to exit ({0}). ".format(errorLevel) if isinstance(errorLevel, int) else "Please press the enter key to exit. ")
		input()
	except:
		pass

def main() -> int:
	# Parameters #
	failureCount = 0
	ecPrivateKeyFilePath = "ecPrivateKey.pem"
	certificateFilePath = "certificate.pem"
	rsaPrivateKeyFilePath = "rsaPrivateKey.pem"
	oldRsaPrivateKeyFilePath = "oldRsaPrivateKey.pem"
	keyboxFilePath = "keybox.xml"
	
	# First-phase Generation #
	failureCount += execute("openssl ecparam -name prime256v1 -genkey -noout -out \"{0}\"".format(ecPrivateKeyFilePath)) != 0
	failureCount += execute("openssl req -new -x509 -key \"{0}\" -out {1} -days 3650 -subj \"/CN=Keybox\"".format(ecPrivateKeyFilePath, certificateFilePath)) != 0
	failureCount += execute("openssl genrsa -out \"{0}\" 2048".format(rsaPrivateKeyFilePath)) != 0
	if failureCount > 0:
		print("Cannot generate a sample ``keybox.xml`` file since {0} PEM file{1} not generated successfully. ".format(failureCount, ("s were" if failureCount > 1 else " was")))
		pressTheEnterKeyToExit(EOF)
		return EOF
	
	# First-phase Reading #
	try:
		with open(ecPrivateKeyFilePath, "r", encoding = "utf-8") as f:
			ecPrivateKey = f.read()
		with open(certificateFilePath, "r", encoding = "utf-8") as f:
			certificate = f.read()
		with open(rsaPrivateKeyFilePath, "r", encoding = "utf-8") as f:
			rsaPrivateKey = f.read()
	except BaseException as e:
		print("Failed to read one or more of the PEM files. Details are as follows. \n{0}".format(e))
		pressTheEnterKeyToExit(EOF)
		return EOF
	
	# Second-phase Generation #
	if rsaPrivateKey.startswith("-----BEGIN PRIVATE KEY-----"):
		print("A newer openssl version is used. The RSA private key in the PKCS8 format will be converted to that in the PKCS1 format soon. ")
		failureCount += execute("openssl rsa -in \"{0}\" -out \"{1}\" -traditional".format(rsaPrivateKeyFilePath, oldRsaPrivateKeyFilePath))
		if failureCount > 0:
			print("Cannot convert the RSA private key in the PKCS8 format to that in the PKCS1 format. ")
			pressTheEnterKeyToExit(EOF)
			return EOF
		else:
			print("Finished converting the RSA private key in the PKCS8 format to that in the PKCS1 format. ")
			try:
				with open(oldRsaPrivateKeyFilePath, "r", encoding = "utf-8") as f:
					rsaPrivateKey = f.read()
			except BaseException as e:
				print("Failed to update the RSA private key from \"{0}\". Details are as follows. \n{1}".format(oldRsaPrivateKeyFilePath, e))
				pressTheEnterKeyToExit(EOF)
				return EOF
	
	# Keybox Generation #
	keybox = keyboxFormatter.format(ecPrivateKey, certificate, rsaPrivateKey)
	print(keybox)
	try:
		with open(keyboxFilePath, "w", encoding = "utf-8") as f:
			f.write(keybox)
		print("Successfully wrote the keybox to \"{0}\". ".format(keyboxFilePath))
		pressTheEnterKeyToExit(EXIT_SUCCESS)
		return EXIT_SUCCESS
	except BaseException as e:
		print("Failed to write the keybox to \"{0}\". Details are as follows. \n{1}".format(keyboxFilePath, e))
		pressTheEnterKeyToExit(EXIT_FAILURE)
		return EXIT_FAILURE



if "__main__" == __name__:
	exit(main())
```

替换 ``/data/adb/tricky_store/keybox.xml`` 之前，记得先将原来的 ``keybox.xml``（刷入 tricky_store 时自带的那个基于 AOSP 的 keybox.xml）备份为 ``keybox.xml.bak``。
![截图](https://i-blog.csdnimg.cn/direct/a413d497d4f8446ba21525008911db48.jpeg)
12月14日凌晨做了一些更新：
1) 支持粗略检查三个子密钥文件内容，支持 OpenSSL 私钥转 RSA 私钥；
2) 如果文件存在，程序会提示是否覆盖；
3) 设备ID随机生成。

```
import os
from random import randint, choice
from base64 import b64decode
try:
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
except:
	pass
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)
LB = 2 # the lower bound of the length of the device ID
UB = 12 # the upper bound of the length of the device ID
CHARSET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
keyboxFormatter = """<?xml version="1.0"?>
<AndroidAttestation>
<NumberOfKeyboxes>1</NumberOfKeyboxes>
<Keybox DeviceID="{0}">
<Key algorithm="ecdsa">
<PrivateKey format="pem">
{1}</PrivateKey>
<CertificateChain>
<NumberOfCertificates>1</NumberOfCertificates>
<Certificate format="pem">
{2}</Certificate>
</CertificateChain>
</Key>
<Key algorithm="rsa">
<PrivateKey format="pem">
{3}</PrivateKey>
</Key>
</Keybox>
</AndroidAttestation>
"""


def canOverwrite(flags:list, idx:int, prompts:str|tuple|list|set) -> bool:
	if isinstance(flags, list) and isinstance(idx, int) and -len(flags) <= idx < len(flags) and isinstance(prompts, (str, tuple, list, set)):
		try:
			if isinstance(prompts, str):
				print("\"{0}\"".format(prompts))
				choice = input("The file mentioned above exists. Overwrite or not [aYn]? ")
			else:
				print(prompts)
				choice = input("At least one of the files mentioned above exists. Overwrite or not [aYn]? ")
			if choice.upper() == "A":
				for i in range((idx if idx >= 0 else len(flags) + idx), len(flags)): # overwirte the current file and all the following necessary files no matter whether they exist
					flags[i] = True
				return True
			elif choice.upper() == "N":
				return False
			else:
				flags[idx] = True
				return True
		except BaseException as e:
			print(e)
			return False
	else:
		input("#")
		return False

def execute(commandline:str) -> int|None:
	if isinstance(commandline, str):
		print("$ " + commandline)
		return os.system(commandline)
	else:
		return None

def handleOpenSSL(flag:bool = True) -> bool|None:
	if isinstance(flag, bool):
		errorLevel = execute("openssl version")
		if EXIT_SUCCESS == errorLevel:
			return True
		elif flag: # can try again
			execute("sudo apt-get install openssl libssl-dev")
			return handleOpenSSL(False)
		else:
			return False
	else:
		return None

def pressTheEnterKeyToExit(errorLevel:int|None = None):
	try:
		print("Please press the enter key to exit ({0}). ".format(errorLevel) if isinstance(errorLevel, int) else "Please press the enter key to exit. ")
		input()
	except:
		pass

def main() -> int:
	# Parameters #
	failureCount = 0
	deviceID = "".join([choice(CHARSET) for _ in range(randint(LB, UB))]) # or specify the device ID manually like "YourDeviceID"
	ecPrivateKeyFilePath = "ecPrivateKey.pem"
	certificateFilePath = "certificate.pem"
	rsaPrivateKeyFilePath = "rsaPrivateKey.pem"
	keyboxFilePath = "keybox.xml" # None for no files written
	flags = [not (os.path.isfile(ecPrivateKeyFilePath) or os.path.isfile(certificateFilePath)), not os.path.isfile(rsaPrivateKeyFilePath), not os.path.isfile(keyboxFilePath)]
	
	# First-phase Generation #
	if flags[0] or canOverwrite(flags, 0, (ecPrivateKeyFilePath, certificateFilePath)):
		failureCount += execute("openssl ecparam -name prime256v1 -genkey -noout -out \"{0}\"".format(ecPrivateKeyFilePath)) != 0
	if flags[0] or not os.path.isfile(certificateFilePath):
		failureCount += execute("openssl req -new -x509 -key \"{0}\" -out {1} -days 3650 -subj \"/CN=Keybox\"".format(ecPrivateKeyFilePath, certificateFilePath)) != 0
	if flags[1] or canOverwrite(flags, 1, rsaPrivateKeyFilePath):
		failureCount += execute("openssl genrsa -out \"{0}\" 2048".format(rsaPrivateKeyFilePath)) != 0
	if failureCount > 0:
		print("Cannot generate a sample ``keybox.xml`` file since {0} PEM file{1} not generated successfully. ".format(failureCount, ("s were" if failureCount > 1 else " was")))
		pressTheEnterKeyToExit(11)
		return 11
	
	# First-phase Reading #
	try:
		with open(ecPrivateKeyFilePath, "r", encoding = "utf-8") as f:
			ecPrivateKey = f.read()
		with open(certificateFilePath, "r", encoding = "utf-8") as f:
			certificate = f.read()
		with open(rsaPrivateKeyFilePath, "r", encoding = "utf-8") as f:
			rsaPrivateKey = f.read()
	except BaseException as e:
		print("Failed to read one or more of the PEM files. Details are as follows. \n{0}".format(e))
		pressTheEnterKeyToExit(12)
		return 12
	
	# Second-phase Generation #
	if flags[1]: # only updates the key content when the original key is newly generated or updating is allowed
		if rsaPrivateKey.startswith("-----BEGIN PRIVATE KEY-----") and rsaPrivateKey.rstrip().endswith("-----END PRIVATE KEY-----"):
			print("A newer openssl version is used. The RSA private key in the PKCS8 format will be converted to that in the PKCS1 format soon. ")
			failureCount += execute("openssl rsa -in \"{0}\" -out \"{0}\" -traditional".format(rsaPrivateKeyFilePath))
			if failureCount > 0:
				print("Cannot convert the RSA private key in the PKCS8 format to that in the PKCS1 format. ")
				pressTheEnterKeyToExit(13)
				return 13
			else:
				print("Finished converting the RSA private key in the PKCS8 format to that in the PKCS1 format. ")
				try:
					with open(rsaPrivateKeyFilePath, "r", encoding = "utf-8") as f:
						rsaPrivateKey = f.read()
				except BaseException as e:
					print("Failed to update the RSA private key from \"{0}\". Details are as follows. \n{1}".format(rsaPrivateKeyFilePath, e))
					pressTheEnterKeyToExit(14)
					return 14
		elif rsaPrivateKey.startswith("-----BEGIN OPENSSH PRIVATE KEY-----") and rsaPrivateKey.rstrip().endswith("-----END OPENSSH PRIVATE KEY-----"):
			print("An OpenSSL private key is detected, which will be converted to the RSA private key soon. ")
			failureCount += execute("ssh-keygen -p -m PEM -f \"{0}\" -N \"\"".format(rsaPrivateKeyFilePath))
			if failureCount > 0:
				print("Cannot convert the OpenSSL private key to the RSA private key. ")
				pressTheEnterKeyToExit(15)
				return 15
			else:
				print("Finished converting the OpenSSL private key to the RSA private key. ")
				try:
					with open(rsaPrivateKeyFilePath, "r", encoding = "utf-8") as f: # the ``ssh-keygen`` overwrites the file though no obvious output filepaths specified
						rsaPrivateKey = f.read()
				except BaseException as e:
					print("Failed to update the RSA private key from \"{0}\". Details are as follows. \n{1}".format(rsaPrivateKeyFilePath, e))
					pressTheEnterKeyToExit(16)
					return 16
	
	# Brief Checks #
	if not (ecPrivateKey.startswith("-----BEGIN EC PRIVATE KEY-----") and ecPrivateKey.rstrip().endswith("-----END EC PRIVATE KEY-----")):
		print("An invalid EC private key is detected. Please try to use the latest key generation tools to solve this issue. ")
		pressTheEnterKeyToExit(17)
		return 17
	if not (certificate.startswith("-----BEGIN CERTIFICATE-----") and certificate.rstrip().endswith("-----END CERTIFICATE-----")):
		print("An invalid certificate is detected. Please try to use the latest key generation tools to solve this issue. ")
		pressTheEnterKeyToExit(18)
		return 18
	if not (rsaPrivateKey.startswith("-----BEGIN RSA PRIVATE KEY-----") and rsaPrivateKey.rstrip().endswith("-----END RSA PRIVATE KEY-----")):
		print("An invalid final RSA private key is detected. Please try to use the latest key generation tools to solve this issue. ")
		pressTheEnterKeyToExit(19)
		return 19
	
	# Keybox Generation #
	keybox = keyboxFormatter.format(deviceID, ecPrivateKey, certificate, rsaPrivateKey)
	print("Generated keybox with a length of {0}: ".format(len(keybox)))
	print(keybox)
	if keyboxFilePath is not None and (flags[2] or canOverwrite(flags, 2, keyboxFilePath)):
		try:
			with open(keyboxFilePath, "w", encoding = "utf-8") as f:
				f.write(keybox)
			print("Successfully wrote the keybox to \"{0}\". ".format(keyboxFilePath))
			pressTheEnterKeyToExit(EXIT_SUCCESS)
			return EXIT_SUCCESS
		except BaseException as e:
			print("Failed to write the keybox to \"{0}\". Details are as follows. \n{1}".format(keyboxFilePath, e))
			pressTheEnterKeyToExit(20)
			return 20
	else:
		print("The keybox has not been written to any files. Please refer to the text above. ")
		pressTheEnterKeyToExit(EXIT_FAILURE)
		return EXIT_FAILURE



if "__main__" == __name__:
	exit(main())
```

顺便摆上 GitHub 链接：[https://github.com/TMLP-Team/keyboxGenerator](https://github.com/TMLP-Team/keyboxGenerator)，我发现这是唯一一个 GitHub 获得的 star 比 CSDN 获得的点赞收藏数之和还多的项目，看来是境外比较需要非 AOSP 但又能过新 BASIC 完整性的 keybox。
