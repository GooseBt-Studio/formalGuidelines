测试[一些密码学方案](https://github.com/xuehuan-yang/PSME/blob/main/src/common/image.py)需要用到 Crypto 库，网上教程大多针对 Windows 和 Python 3.10 或以下的环境，所以写下了这篇博文。

## 部署与使用

首先执行 ``su`` 输入密码进入超级用户，部署完 Python 3.12 环境后，执行以下命令进行安装（如果之前有安装过旧版可能需要先进行清除具体操作请参考其它教程）。
```
apt-get install python3-pycryptodome
```
![安装](https://i-blog.csdnimg.cn/direct/afd208133d124dbd8594f99332672647.png)


执行以下命令进行测试，看到 ok 就行啦！
```
python3 -m Cryptodome.SelfTest
```
![测试](https://i-blog.csdnimg.cn/direct/2c1a7c47e7b3403fa8daeb7721cdcc8b.png)

使用时，需要将 Crypto 替换为 Cryptodome，例如，需要将 ``from Crypto.Cipher import AES`` 修改为 ``from Cryptodome.Cipher import AES``。

## 反思

发现在 Ubuntu 24.04.1 LTS | Python 3.12 环境下很多 Python 库的安装命令都变成了 ``apt-get install python3-XXX`` 的形式，例如安装 ``pandas`` 从 ``python3 -m pip install pandas`` 变成了 ``apt-get install python3-pandas``。

一方面，Python 的库安装需要超级用户（Linux）或管理员（Windows）权限，缺乏足够的权限很可能导致 defaulting to XXX 的局面，随后就是包装得到处都是；另一方面，在 Linux 操作系统上，Python 官方提示使用 root 进行 Python 的库安装会产生较高的风险。所以，能够理解，在 Linux 操作系统上，Python 3.12 将 Python 的库管理托管给 apt 进行，这样既解决了权限问题，又降低了以 root 身份执行 Python 库安装的风险。

## 参考文献

- [https://blog.csdn.net/weixin_55024601/article/details/136062283](https://blog.csdn.net/weixin_55024601/article/details/136062283)
- [https://pycryptodome.readthedocs.io/en/latest/src/installation.html](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)
