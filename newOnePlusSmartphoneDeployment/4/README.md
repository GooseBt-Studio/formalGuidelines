### 其它

如需 root 和安装 LSPosed 框架，可跟随 [https://github.com/LRFP-Team/LRFP/tree/main/Implementers](https://github.com/LRFP-Team/LRFP/tree/main/Implementers) 中的教程。
如需过检，可跟随 [https://github.com/LRFP-Team/LRFP/tree/main/Bypassers](https://github.com/LRFP-Team/LRFP/tree/main/Bypassers) 中的教程。

截至 2026 年 6 月 2 日，最新长期支持版（LTS）的 JDK 是 25。
考虑到在 Termux 上直接通过系统提供的 ``pkg``、``apt`` 或 ``apt-get`` 安装 Python 会导致 pip 被系统的包管理器接管，造成极大的不便。
于是，在各种 GenAI 的助力下，我们找出了最好的最新版 Python（含测试版）部署方案，结合对 git、gh 和 JDK 的安装，其命令如下。

```shell
pkg update && pkg upgrade -y
pkg install -y clang gh git make openjdk-25 wget
major="$(curl -s https://www.python.org/ftp/python/ | grep -oP 'href="\K[0-9]+\.[0-9]+(\.[0-9]+)?(?=/")' | sort -V | tail -n 1)"
minor="$(curl -s "https://www.python.org/ftp/python/${major}/" | grep -oP 'href="\KPython-[0-9]+\.[0-9]+(\.[0-9]+[a-z0-9]*)?\.tgz' | sort -V | tail -n 1)"
wget -c "https://www.python.org/ftp/python/${major}/${minor}"
tar -xf "${minor}"
cd "${minor%.tgz}"
ac_cv_func_close_range=no ac_cv_func_copy_file_range=no ac_cv_func_fexecve=no ac_cv_func_getloadavg=no ac_cv_func_getlogin_r=no ac_cv_func_getpwent=no ac_cv_func_posix_spawn=no ac_cv_func_posix_spawnp=no ac_cv_func_preadv2=no ac_cv_func_pthread_getname_np=no ac_cv_func_pwritev2=no ac_cv_func_sem_clockwait=no ac_cv_func_statx=no ac_cv_header_spawn_h=no ./configure --prefix=${PREFIX} --with-ensurepip=install --with-openssl=${PREFIX} --with-system-expat
make -j$(nproc)
make install
ln -s "${PREFIX}/bin/python3" "${PREFIX}/bin/python"
ln -s "${PREFIX}/bin/python" "${PREFIX}/bin/py"
ln -s "${PREFIX}/bin/pip3" "${PREFIX}/bin/pip"
python -m pip install --upgrade pip
python -m pip install wheel
exit
```

在未来，若出现了更新的长期支持版的 JDK，可将 ``openjdk-`` 后的版本号进行相应的更换。

若要在标准的 Ubuntu 或 WSL 下的 Ubuntu 中执行上述命令，请以 root 身份执行，将 ``pkg`` 更改为 ``apt-get``，
将最长的一行（``./configure`` 步骤）修改为 ``./configure --prefix=/usr/local --enable-optimizations --with-ensurepip=install``，
并在执行 ``make install`` 后执行以下命令。

```shell
PREFIX=/usr/local
cat > ~/.config/pip/pip.conf << 'EOF'
[global]
root-user-action = ignore
EOF
```
