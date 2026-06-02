### 其它

如需 root 和安装 LSPosed 框架，可跟随 [https://github.com/LRFP-Team/LRFP/tree/main/Implementers](https://github.com/LRFP-Team/LRFP/tree/main/Implementers) 中的教程。
如需过检，可跟随 [https://github.com/LRFP-Team/LRFP/tree/main/Bypassers](https://github.com/LRFP-Team/LRFP/tree/main/Bypassers) 中的教程。

考虑到在 Termux 上直接通过系统提供的 ``pkg``、``apt`` 或 ``apt-get`` 安装 Python 会导致 pip 被系统的包管理器接管，造成极大的不便。
于是，在各种 GenAI 工具的助力下，我们找出了最好的最新版 Python（含测试版）部署方案，结合对最新版 git、gh 和 JDK 的安装，其命令如下。请尽可能在最原始的 Termux 环境中执行。

```shell
pkg update && pkg upgrade -y
pkg install -y clang gh git make "$(apt-cache search '^openjdk-[0-9]+$' | grep -oE 'openjdk-[0-9]+' | sort -V | tail -n 1)" wget
major="$(curl -s https://www.python.org/ftp/python/ | grep -oP 'href="\K[0-9]+\.[0-9]+(\.[0-9]+)?(?=/")' | sort -V | tail -n 1)"
minor="$(curl -s "https://www.python.org/ftp/python/${major}/" | grep -oP 'href="\KPython-[0-9]+\.[0-9]+(\.[0-9]+[a-z0-9]*)?\.tgz' | sort -V | tail -n 1)"
wget -c "https://www.python.org/ftp/python/${major}/${minor}"
tar -xf "${minor}"
cd "${minor%.tgz}"
ac_cv_func_close_range=no ac_cv_func_copy_file_range=no ac_cv_func_fexecve=no ac_cv_func_getloadavg=no ac_cv_func_getlogin_r=no ac_cv_func_getpwent=no \
ac_cv_func_posix_spawn=no ac_cv_func_posix_spawnp=no ac_cv_func_preadv2=no ac_cv_func_pthread_getname_np=no ac_cv_func_pwritev2=no ac_cv_func_sem_clockwait=no \
ac_cv_func_statx=no ac_cv_header_spawn_h=no ./configure --prefix=${PREFIX} --with-ensurepip=install --with-openssl=${PREFIX} --with-system-expat
make -j$(nproc)
make install
ln -s "${PREFIX}/bin/python3" "${PREFIX}/bin/python"
ln -s "${PREFIX}/bin/python" "${PREFIX}/bin/py"
ln -s "${PREFIX}/bin/pip3" "${PREFIX}/bin/pip"
python -m pip install --upgrade pip
python -m pip install wheel
```

请在执行过程中保持网络通畅，如某条命令执行失败，请重试，或询问 GenAI 工具以寻求帮助。
在未来，若需要使用 git，可执行 ``gh auth login`` 进行身份认证。在登录了多个 GitHub 账号的情况下，可执行 ``gh auth switch`` 切换激活的账号。

若要在干净的 Ubuntu（含 WSL 下的 Ubuntu）中实现与上述命令类似所达到的类似的效果，请以 root 身份执行以下命令。

```shell
apt-get update && apt-get upgrade -y
apt-get install -y clang gh git make "$(apt-cache search '^openjdk-[0-9]+$-jdk' | grep -oE 'openjdk-[0-9]+-jdk' | sort -V | tail -n 1)" wget
major="$(curl -s https://www.python.org/ftp/python/ | grep -oP 'href="\K[0-9]+\.[0-9]+(\.[0-9]+)?(?=/")' | sort -V | tail -n 1)"
minor="$(curl -s "https://www.python.org/ftp/python/${major}/" | grep -oP 'href="\KPython-[0-9]+\.[0-9]+(\.[0-9]+[a-z0-9]*)?\.tgz' | sort -V | tail -n 1)"
wget -c "https://www.python.org/ftp/python/${major}/${minor}"
tar -xf "${minor}"
cd "${minor%.tgz}"
PREFIX="/usr/local"
./configure --prefix=${PREFIX} --enable-optimizations --with-ensurepip=install
make -j$(nproc)
make altinstall
ln -s "${PREFIX}/bin/python3" "${PREFIX}/bin/python"
ln -s "${PREFIX}/bin/python" "${PREFIX}/bin/py"
ln -s "${PREFIX}/bin/pip3" "${PREFIX}/bin/pip"
cat > ~/.config/pip/pip.conf << "EOF"
[global]
root-user-action = ignore
EOF
python -m pip install --upgrade pip
python -m pip install wheel
```

同理，请在执行过程中保持网络通畅，如某条命令执行失败，请重试，或询问 GenAI 工具以寻求帮助。
此处，设置 ``PREFIX`` 为 ``/usr/local`` 而非 ``/usr`` 是因为 ``/usr/bin/`` 下的文件一般为系统安装的，而 ``/usr/local/bin/`` 下的文件则一般为超级用户手动安装的。
使用 ``make altinstall`` 是为了避免与系统自带的 Python 发生冲突，但如果事先已确认系统层的 Python 已被清理干净或 Ubuntu 处于刚安装完成且没有自带 Python 的状态，则可以使用 ``make install``。

更多有关在标准的 Ubuntu 或 WSL 下的 Ubuntu 中安装 Python 的命令，可参阅 [https://github.com/yueryang/Cryptography-Schemes](https://github.com/yueryang/Cryptography-Schemes)。

在根据自己的偏好设置完系统设置、登录完各种境内外应用（如微信、QQ、Telegram、WhatsApp 和 Swift Backup）和导入数据后，这台一加手机就基本可以投入日常使用了。
