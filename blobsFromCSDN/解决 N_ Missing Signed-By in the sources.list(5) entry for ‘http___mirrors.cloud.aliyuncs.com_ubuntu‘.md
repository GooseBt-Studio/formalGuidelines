如题，本文旨在解决 ``N: Missing Signed-By in the sources.list(5) entry for 'http://mirrors.cloud.aliyuncs.com/ubuntu'`` 的报错问题。该报错出现于某次 Ubuntu 24.04.1 LTS 更新后，报错信息如图所示。
![报错](https://i-blog.csdnimg.cn/direct/739af42b0fa8472e87065b7e72db25df.png)
参阅 [https://blog.csdn.net/qq_36433118/article/details/143329284](https://blog.csdn.net/qq_36433118/article/details/143329284) 执行，发现笔者的机器上没有 ``/etc/apt/sources.list.d/ubuntu.sources`` 文件。
![文件不存在](https://i-blog.csdnimg.cn/direct/bb20947380a1409385b9294e1c6778ac.png)
于是，尝试直接新建一个文件。在 [https://cn.linux-console.net/?p=31032](https://cn.linux-console.net/?p=31032) 找到了可复制的 ``.sources`` 文件代码，使用 ``vim`` 或 ``nano`` 工具将以下代码写入 ``/etc/apt/sources.list.d/ubuntu.sources`` 中。
```
Types: deb
URIs: http://us.archive.ubuntu.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```
运行 ``apt-get update`` 后，发现更新时间变长了，但 ``N: Missing Signed-By in the sources.list(5) entry for 'http://mirrors.cloud.aliyuncs.com/ubuntu'`` 的报错依旧存在。据此，猜测该文件会生效，考虑直接强行将上述源代码中的网址修改为报错网址进行强制覆盖，故修改 ``/etc/apt/sources.list.d/ubuntu.sources`` 为以下内容。
```
Types: deb
URIs: http://mirrors.cloud.aliyuncs.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb
URIs: http://mirrors.cloud.aliyuncs.com/ubuntu/
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```
报错不见了，但出现了一堆如下图所示的警告（Warning）。
![警告](https://i-blog.csdnimg.cn/direct/954bbfcb21bb4668be88fc1d517e0b03.png)
看大概意思，应该是网址重复了，而且考虑到即使原本没有 ``ubuntu.sources``，命令 ``apt-get update`` 执行时依旧会解析报错网址 ``http://mirrors.cloud.aliyuncs.com/ubuntu/``。这说明应该还有其他 ``.sources`` 文件在起作用。于是，cd 到 ``/etc/apt/sources.list.d/ubuntu.sources`` 后执行 ``ls`` 发现存在一个以 ``.sources`` 结尾的文件。打开一看，果然，上述猜测是正确的。将 ``Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg`` 添加到该文件中每一个没有 ``Signed-By`` 字段的结构体里，保存退出后，重新 ``apt-get update``，问题解决。
![问题解决](https://i-blog.csdnimg.cn/direct/fca178106c3a4d9f8cd527c124b65a90.png)
另外，如有需要，友友们可以将以下代码拿去。如果还有更复杂的情况，或许清空目录 ``/etc/apt/sources.list.d``，随后建一个 ``.sources`` 文件写入以下内容就能解决问题。当然，该解决方案仅对 Ubuntu 24.04.1 LTS 的操作系统生效，且笔者仅在阿里云服务器上进行过测试。使用 Ubuntu 24.04.1 LTS 服务器但不在阿里云服务器上的朋友们可以在考虑使用阿里源的同时考虑使用其它源（如清华源）。
```
Types: deb deb-src
URIs: http://mirrors.cloud.aliyuncs.com/ubuntu/
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

Types: deb deb-src
URIs: http://mirrors.cloud.aliyuncs.com/ubuntu
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

```
