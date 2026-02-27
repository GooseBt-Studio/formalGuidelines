enRSA，以后遇到 CTF 新生赛做 RSA，直接用这个 Python 脚本吧！一劳永逸！除非分解因素的库不工作了。

```
import os
from sys import argv, exit, stdin
from msvcrt import getch
PLATFORM = __import__("platform").system().lower()
EXIT_SUCCESS = 0
EXIT_FAILURE = 1
EOF = (-1)


def clearScreen(fakeClear = 120): # 虚假的清屏函数
	if stdin.isatty(): # 在终端
		if "windows" == PLATFORM:
			os.system("cls")
		elif "linux" == PLATFORM:
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

def fixlib(cb, command): # 定义库处理函数
	print("未（正确）安装 " + cb + " 库，正在尝试执行安装，请确保您的网络连接正常。")
	os.system("py -m pip install " + cb)
	try:
		exec(command)
	except:
		clearScreen()
		if "windows" == PLATFORM and os.popen("ver").read().upper().find("XP") == -1:
			print("安装 " + cb + " 库失败，正在尝试以管理员权限执行安装，请确保您的网络连接正常。")
			os.system("mshta vbscript:createobject(\"shell.application\").shellexecute(\"py\",\"-m pip install "+cb+"\",\"\",\"runas\",\"1\")(window.close)")
			print("已弹出新窗口，确认授权并安装完成后，请按任意键继续。")
			getch()
			try:
				exec(command)
			except:
				print("无法正确安装 " + cb + " 库，请按任意键退出，建议稍后重新启动本程序。")
				getch()
				clearScreen()
				exit()
		else:
			print("无法正确安装 " + cb + " 库，请按任意键退出，建议稍后重新启动本程序。")

def egcd(a, b): # 定义算法函数
	if a == 0:
		return b, 0, 1
	else:
		g, y, x = egcd(b % a, a)
		return g, x - (b // a) * y, y
def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		return -1
	else:
		return x % m
def ne(n, e):
	f = FactorDB(n)
	f.connect()
	result = f.get_factor_list()
	if len(result) != 2:
		return -1
	# print(result)
	p, q = result[0], result[1]
	print("p =", p)
	# p = 14001864863580621636769
	print("q =", q)
	# q = 14901278358136141983377
	d = modinv(e, (p - 1) * (q - 1))
	return d

# 定义帮助函数
def help(option) -> int:
	print()
	if option != "/?" and option != "-?":
		print("\a错误：无效的命令行参数—“" + str(option) + "”。")
	print("描述：给定n和e的RSA解密运算。\n\n参数列表：\n\t/n\t\t设置n的值\n\t/e\t\t设置e的值\n\t[n]\t\tn的值\n\t[e]\t\te的值\n\t[c]\t\tc的值（可选）\n")
	print("命令行格式：\n\tenRSA.py /n [n] /e [e] /c [c]\n")
	print("示例：")
	print("\tenRSA.py /n 208645685865220781237677030108874331729988913 /e 10111111111")
	print("\tenRSA.py /n 52325875250719834038466049947961388071650687620177969152235704766211385392939 /e 65537 /c 34235083603255394631472769355891395597556301609076426725471325009186091570619\n")
	if option.lower() in ("/?", "-?", "?", "/h", "-h", "h", "/help", "--help", "help"):
		return EXIT_SUCCESS
	else:
		return EOF

# 处理命令行参数
if "/?" in argv or "-?" in argv:
	exit(help("/?"))
if len(argv) in (5, 7):
	if argv[1].lower() in ("/n", "-n", "n"):
		try:
			n = int(argv[2])
			assert(n >= 4)
		except:
			print("\a错误：提供的 n 值不正确。\n")
			exit(EOF)
	elif argv[1].lower() in ("/e", "-e", "e"):
		try:
			e = int(argv[2])
			assert(e >= 1)
		except:
			print("\a错误：提供的 e 值不正确。\n")
			exit(EOF)
	elif argv[1].lower() in ("/c", "-c", "c"):
		try:
			c = int(argv[2])
			assert(c >= 0)
		except:
			print("\a错误：提供的 c 值不正确。\n")
			exit(EOF)
	if argv[3].lower() in ("/n", "-n", "n"):
		try:
			n = int(argv[4])
			assert(n >= 4)
		except:
			print("\a错误：提供的 n 值不正确。\n")
			exit(EOF)
	elif argv[3].lower() in ("/e", "-e", "e"):
		try:
			e = int(argv[4])
			assert(e >= 1)
		except:
			print("\a错误：提供的 e 值不正确。\n")
			exit(EOF)
	elif argv[3].lower() in ("/c", "-c", "c"):
		try:
			c = int(argv[4])
			assert(c >= 0)
		except:
			print("\a错误：提供的 e 值不正确。\n")
			exit(EOF)
	if len(argv) == 7:
		if argv[5].lower() in ("/n", "-n", "n"):
			try:
				n = int(argv[6])
				assert(n >= 4)
			except:
				print("\a错误：提供的 n 值不正确。\n")
				exit(EOF)
		elif argv[5].lower() in ("/e", "-e", "e"):
			try:
				e = int(argv[6])
				assert(e >= 1)
			except:
				print("\a错误：提供的 e 值不正确。\n")
				exit(EOF)
		elif argv[5].lower() in ("/c", "-c", "c"):
			try:
				c = int(argv[6])
				assert(c >= 0)
			except:
				print("\a错误：提供的 e 值不正确。\n")
				exit(EOF)
	try:
		print("n =", n)
	except:
		print("\a错误：未定义 n。")
		exit(EOF)
	try:
		print("e =", e)
	except:
		print("\a错误：未定义 e。")
		exit(EOF)
	try:
		print("c =", c)
	except:
		c = None
	try:
		from factordb.factordb import FactorDB
	except:
		fixlib("factordb-pycli", "from factordb.factordb import FactorDB")
		from factordb.factordb import FactorDB
	d = int(ne(n, e))
	if d == -1:
		print("\a错误：输入的 n、e 值无效，或密钥不是线性的。")
		exit(-1)
	else:
		print("d =", d, "\n")
		exit(0)
elif len(argv) != 1:
	exit(help(argv[1:]))

# 主程序
if stdin.isatty(): # 在终端
	os.system("title 给定 n 和 e 的 RSA 解密运算&color e")
clearScreen()
try:
	from factordb.factordb import FactorDB
except:
	fixlib("factordb-pycli", "from factordb.factordb import FactorDB")
	from factordb.factordb import FactorDB
while True:
	clearScreen()
	while True:
		try:
			clearScreen()
			n = int(input("请输入 n："))
			assert(n >= 4)
			break
		except:
			clearScreen()
			print("\a输入的 n 不合法，请按任意键重新输入。")
			getch()
	while True:
		try:
			clearScreen()
			print("n = {0}".format(n))
			e = int(input("请输入 e："))
			assert(e >= 1)
			break
		except:
			clearScreen()
			print("\a输入的 e 不合法，请按任意键重新输入。")
			getch()
	while True:
		try:
			clearScreen()
			print("n = {0}".format(n))
			print("e = {0}".format(e))
			c = input("请输入 c（直接回车可跳过）：")
			if c:
				c = int(c)
				assert(c >= 0)
			else:
				c = None
			break
		except:
			clearScreen()
			print("\a输入的 e 不合法，请按任意键重新输入。")
			getch()
	
	clearScreen()
	print("n =", n)
	print("e =", e)
	# n = 208645685865220781237677030108874331729988913
	# e = 10111111111
	try:
		d = int(ne(n, e))
		# d = 197944482226238981644771241465020009358173687
		if d == -1:
			print("\a错误：输入的 n、e 值无效，或密钥不是线性的。")
		else:
			print("d =", d)
			if c is not None:
				print("m =", pow(c, d , n))		
	except:
		print("\a错误：网络连接失败，无法获取爆破资源。")
	print("\n\n输入“exit”（不区分大小写）回车退出程序，输入其它或直接回车运行新运算。")
	Ens = input("")
	if Ens.lower() == "exit":
		clearScreen()
		exit(EXIT_SUCCESS)
```
