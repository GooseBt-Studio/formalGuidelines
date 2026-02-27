# 1. 在 Windows 11 上部署 Ubuntu (WSL)
由于作者没有高性能的 Ubuntu 服务器或个人电脑，且公司或学校提供的 Ubuntu 服务器虽然提供高性能 GPU 等硬件配置但通常不会提供 root 权限，因而作者通过在搭载了 Windows 11 的个人电脑上启动 Ubuntu (WSL) 来进行指引。不使用 WSL 的读者朋友可直接跳过本节。

参考 [https://learn.microsoft.com/zh-cn/windows/wsl/install](https://learn.microsoft.com/zh-cn/windows/wsl/install) 完成 WSL 功能启用重启 Windows 11 后，（以管理员身份）启动命令提示符（按下 Win 键后使用英文输入法输入 cmd 三个字母后单击“命令提示符”或“以管理员身份运行”并授权），在弹出的命令提示符窗口（以下简称“cmd 窗口”）中输入 ``wsl --install Ubuntu`` 并回车。随后，根据提示信息输入用户名（建议全部小写字母）、密码（建议十位以上的综合型密码）和确认密码。这里用户名、密码和确认密码的用途是注册，而不是登录。显示出系统信息和其它信息后，“一台” WSL 就安装完成了，我们也进入到了 WSL 中。
![安装 WSL](https://i-blog.csdnimg.cn/direct/c42970a0dc294e69b30c04092ae7f259.png)
此处，我们使用 Ubuntu 24.04.1 LTS，因为这是我个人认为所有公开的 Linux 操作系统中最好用的一个。为方便起见，用户登录到 WSL 后立即使用 ``sudo passwd root`` 命令指定 root 用户的密码。此处，第一个输入的密码为上面我们注册的用户（例如 universe）的密码，用途是确认用户授权；第二个输入的密码为为新 root 用户指定的新密码，用途为用户注册；第三个输入的密码用于再次确认第二次输入的密码，用途是确认当前用户为新 root 用户指定的新密码，防止用户键入到计算机的密码和用户希望键入到计算机的密码不一致或手误。随后，执行 ``su root`` 命令并输入密码切换到 root，执行 ``cd ~`` 切换到 root 用户的用户目录。
![su root](https://i-blog.csdnimg.cn/direct/61bd0569b6e747549cba4c814d291d65.png)
如有需要，执行 ``apt-get update && apt-get upgrade`` 进行一些更新和升级，在询问是否继续升级时输入 ``Y`` 并回车，也可以直接回车（默认 ``Y``）。有需要的用户也可以更改 apt 源。
![apt-get update && apt-get upgrade](https://i-blog.csdnimg.cn/direct/e5cc50fb5f6b42cb8ba386dd986c0dc3.png)
![apt-get update && apt-get upgrade](https://i-blog.csdnimg.cn/direct/b0b1ac116e34478b96f81854bbb7a946.png)
![apt-get update && apt-get upgrade](https://i-blog.csdnimg.cn/direct/5e49bc3026e441e7bfb535a0a8712f14.png)
附：如果需要退出 WSL 的登录返回到 cmd 中，可以直接在 WSL 的 shell 中执行 ``exit``。退出后，WSL 中的数据会保留。如果哪天不需要这个 WSL 了，可以通过在 cmd 下执行 ``wsl --unregister Ubuntu`` 命令进行对 Ubuntu WSL 的注销。相比于 ``wsl --uninstall Ubuntu``，``wsl --unregister Ubuntu`` 会清空该 WSL 中的所有数据并移除该 WSL，而 若在 ``wsl --uninstall Ubuntu`` 执行后重新执行 ``wsl --install Ubuntu``，会发现之前的数据还在。
![注销 WSL](https://i-blog.csdnimg.cn/direct/1561dc2951594feaa46da58f35528722.png)
# 2. 部署 Python
目前（2024 年 12 月 5 日）Ubuntu 上的情况是：
1) 依照官方 repo 中的一个 Issue（[https://github.com/JHUISI/charm/issues/307](https://github.com/JHUISI/charm/issues/307)），charm 的部署需要 Python 3.10 或以下；
2) 使用 ``apt-get`` 直接安装 Python 默认的版本是 Python 3.12，无法使用 ``apt-get`` 直接安装 Python 3.10；
3) 使用 ``apt-get`` 直接安装 Python-dev 的默认版本是 3.12，无法使用 ``apt-get`` 直接安装 Python3.10-dev；
4) 可以使用 ``wget``、``unzip``、``tar``、``make`` 等命令手动安装 Python 3.10，但搜索了一段时间未找到对应的 Python3.10-dev 安装方式；
5) 无 Python-dev 部署 charm 时，提示需要 Python-dev；
6) 有大佬适配了 Python 3.12 的 charm，位于 [https://github.com/EliusSolis/charm](https://github.com/EliusSolis/charm)，以后估计会被 merge 进官方的 charm。

综合以上情况，我们决定用 Python 3.12 和 [https://github.com/EliusSolis/charm](https://github.com/EliusSolis/charm) 中的 charm 进行部署。
直接执行 ``apt-get install python3 python3-dev python-is-python3``，回车确认，完成安装。
![安装 Python](https://i-blog.csdnimg.cn/direct/dd4cfbe4d768488eb12bd9958cc321dc.png)
运行 ``python`` 进行检查，发现正常。
![python](https://i-blog.csdnimg.cn/direct/5172065c438242b990f2feec9010621c.png)
输入 ``quit()`` 退出 Python，返回到 WSL 的终端。
# 3. GMP
翻阅 charm 官方安装说明 [https://github.com/JHUISI/charm/blob/dev/README.md](https://github.com/JHUISI/charm/blob/dev/README.md) 可知 charm 的部署依赖于 GMP 5.x。不过，GMP 官网（[https://gmplib.org/](https://gmplib.org/)）目前最新版已经是 6.3.0 了。经测试，GMP 6.3.0 也可以，所以，此处使用 GMP 6.3.0。如果有更新版本，请相应替换本节剩余内容中的版本号。
右键单击以下网页截图中箭头指向的位置，复制链接，得到如 ``https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz`` 的链接。在 Ubuntu 中执行 ``wget https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz`` 下载，使用 ``tar -xf gmp-6.3.0.tar.xz`` 或 ``tar -xvf gmp-6.3.0.tar.xz``（显示详细信息）进行解压。也可以下载其它格式，参考 [https://rpubs.com/xliusufe/gmp](https://rpubs.com/xliusufe/gmp) 进行解压。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/13c182abdcc24a1e98f14811dfccb013.png)
![GMP](https://i-blog.csdnimg.cn/direct/af878ab5f0d94e6d85258cada8518843.png)
解压后，使用 ``cd gmp-6.3.0`` 进入 gmp-6.3.0 目录。由于需要编译 C/C++ 程序以及 m4，故：
1) 执行 ``apt-get install gcc g++`` 安装 gcc 和 g++；
2) 执行 ``apt-get install m4`` 安装 m4；
3) 执行 ``apt-get install make`` 安装 make。

执行 ``./configure --prefix=/usr --enable-cxx``，其中，第一个参数为更改默认搜索目录为 ``/usr``，第二个参数为启用 C++ 支持。如果提示权限不足（Permisson denied），请先尝试先执行 ``chmod +x ./configure``；如果出现 ``configure: error: could not find a working compiler, see config.log for details``、``configure: error: No usable m4 in $PATH or /usr/5bin (see config.log for reasons).`` 和 ``Command 'make' not found`` 之类的错误提示，那一般就是上面的包没安装好，可以尝试重新执行上面的安装命令，或者卸载重装。
![gcc 和 g++](https://i-blog.csdnimg.cn/direct/b23e53ced7d04590974dd8b09169b63c.png)
![m4](https://i-blog.csdnimg.cn/direct/3742888bc5764daaa2c22b569c21d24f.png)
![make](https://i-blog.csdnimg.cn/direct/d10824b7fffa481b92dfb675f0c5fa90.png)
在命令 ``./configure --enable-cxx`` 执行完成并成功后，依次运行 ``make``、``make check`` 和 ``make install``，其中，可以在 ``make check`` 时检查下是否存在错误或者警告。以下截取了 ``make check`` 过程中的一些绿色的 PASS，看着很开心。这三个命令的执行耗时累计五分钟左右。
![PASS](https://i-blog.csdnimg.cn/direct/ddf9bb7af63a48088d532fe379a755ae.png)
![PASS](https://i-blog.csdnimg.cn/direct/70892841a0f64bcbaab49ebbc92c9116.png)
![make install](https://i-blog.csdnimg.cn/direct/39c1a316b4b7496b8092280877ce5e7c.png)
附：如果在 ``make install`` 之前想修改 ``./configure`` 的参数，可使用 ``make clean`` 进行清理。
# 4. PBC
PBC 库的部署参考于 [https://crypto.stanford.edu/pbc/manual.html](https://crypto.stanford.edu/pbc/manual.html) 和 [https://blog.csdn.net/Frinklin_wang/article/details/123866728](https://blog.csdn.net/Frinklin_wang/article/details/123866728)。
首先，咱们打开 PBC 库的官网 [https://crypto.stanford.edu/pbc/download.html](https://crypto.stanford.edu/pbc/download.html)，找到 Download 下面的表格中的第一个链接，右键复制。
![PBC 官网](https://i-blog.csdnimg.cn/direct/692c13e98db149b6a526ce1d931caefb.png)
使用 ``cd ~`` 返回 root 用户目录，执行 ``wget https://crypto.stanford.edu/pbc/files/pbc-0.5.14.tar.gz`` 下载包。执行 ``tar -zxf pbc-0.5.14.tar.gz`` 或 ``tar -zxvf pbc-0.5.14.tar.gz``（显示详细信息）进行解压。
![PBC](https://i-blog.csdnimg.cn/direct/e4d481a2412b46fea8138f4fd5161eb9.png)
执行 ``apt-get install flex bison`` 并回车确认以安装依赖的包。
![flex 和 bison](https://i-blog.csdnimg.cn/direct/11c1d56723974f08b03b968a10eff1ce.png)
使用 ``cd pbc-0.5.14`` 进入 pbc-0.5.14 目录，执行 ``./configure``。如果提示权限不足（Permission denied），请执行 ``chmod +x ./configure``。在 ``./configure`` 执行成功后，执行 ``make && make install``。
![./configure](https://i-blog.csdnimg.cn/direct/ff0fd431d443458c8f4ae9db866f754c.png)
![make && make install](https://i-blog.csdnimg.cn/direct/524d4c2c4f314cb483788ee690d1df05.png)
![PBC 安装结束](https://i-blog.csdnimg.cn/direct/f3adad32527f4d67ac6193141cbdb864.png)
为测试 pbc 的正确性，使用 ``cd pbc`` 进入 pbc 目录，此时应当位于 ~/pbc-0.5.14/pbc。为方便起见，运行 ``vim test.txt``，按下 ``i`` 键进入编辑模式，将以下内容复制粘贴进去（注意符号都是英文），随后按下键盘左上角的 ESC 键退出编辑模式，输入 ``:x`` 回车退出 vim。顺带声明一下，以下例子来自于本节开头参考的两个链接。
```
g:=rnd(G1);
g;

h:=rnd(G2);
h;

a:=rnd(Zr);
b:=rnd(Zr);
pairing(g^a,g^b);

a:=rnd(Zr);
b:=rnd(Zr);
pairing(g,h)^(a*b);

```
![cd pbc](https://i-blog.csdnimg.cn/direct/21fc0693dbf7499d87ee9ad3db93c5d5.png)
![vim](https://i-blog.csdnimg.cn/direct/98ab61bdb42a40c59b24130e95b3886c.png)
退出 vim 后，可以用 ``cat test.txt`` 查看一下 test.txt 的内容，随后，执行 ``./pbc test.txt``，观察结果。如无意外，一次可能的结果如下：
```
[3329247549575083693704544702300111878032757859527738620078340162954994153076106270578798542088759817755260473344467142914450640537953655213941777251150507, 2915725110970502014368664778822139336115812849055983709686958575727617915386111790813698074081175900851401370141481357430955279929040287141435866041352465]
[3242974909124154401306977997240035331670277658104974758958060345931843939238480034054970695129337969056110321396968088221841267448950244490146519453034952, 4102645750044991539186357580272542381470433262964030405150098834238307121213420471646007670322526602097806928211429728285753402549456577684823579495975023]
[4204905719718175991825854736739721947952505513162738068839979360094249342284680566494097041790152055409462955994730015080480413075607530213740171415894742, 446574590468230745320006695766115100785771408743827211116005662318542764154352629872772863803833470234707075454507234814615174213789732490852008370212665]
[1292042521100579230125067081486676117138594032521849019268142455404207899451482841067146153826541421710150688896771252517403929838056204610903731400443238, 6384245293263856412404284561094069320155145616120241897229969538798442361256734337315733254634859801365184035421441627651994380108240891046561604126951898]
```
![正确性验证](https://i-blog.csdnimg.cn/direct/aba22329ac4c487d8ee68ba2d5b8b601.png)
可以多次执行 ``./pbc test.txt``，但每次结果都是随机的。
![多次执行](https://i-blog.csdnimg.cn/direct/370c95f79a474a45847dfa34ca4bed58.png)
为便于库路径管理，可依次执行以下命令。
```
cd /etc/ld.so.conf.d
echo '/usr/local/lib' > libpbc.conf
cat libpbc.conf
ldconfig
```
![ldconfig](https://i-blog.csdnimg.cn/direct/f98029368d384f188ee65721b7fb62ed.png)
# 5. OpenSSL
使用 ``cd ~`` 返回 root 用户目录。很天真地以为直接 ``apt-get install openssl`` 就可以了。
然而，但是编译错误，说找不到头文件。
参考了下 [https://stackoverflow.com/questions/3016956/how-do-i-install-the-openssl-libraries-on-ubuntu](https://stackoverflow.com/questions/3016956/how-do-i-install-the-openssl-libraries-on-ubuntu)，需要执行 ``apt-get install libssl-dev``，因为要安装的是 lib。还好，也是一个命令的事情。
![OpenSSL](https://i-blog.csdnimg.cn/direct/9218f11771174612b6b954f7c1b97ce6.png)
在 [https://github.com/EliusSolis/charm](https://github.com/EliusSolis/charm) 中找到了链接 [https://github.com/EliusSolis/charm.git](https://github.com/EliusSolis/charm.git)，发现 Ubuntu 自带了 git。于是，直接使用 ``git clone https://github.com/EliusSolis/charm.git``。
![git clone](https://i-blog.csdnimg.cn/direct/49c43fbd70e44c21a7f055aa32d20336.png)
依次执行以下命令完成部署。
```
# chmod +x ./configure
./configure
make install
make test
```
![make install](https://i-blog.csdnimg.cn/direct/7299f56357d9433fb612486344344186.png)
执行到 ``make test`` 时出现了以下意外。
```
/usr/bin/python: No module named pip
error: Command '['/usr/bin/python', '-m', 'pip', '--disable-pip-version-check', 'wheel', '--no-deps', '-w', '/tmp/tmp_srxsing', '--quiet', 'pytest']' returned non-zero exit status 1.
make: *** [Makefile:51: test] Error 1
```
原来是，Python 3.12 的 pip 不会随着 Python 的安装而安装了。事实上，大概从这时候开始，在 Linux 操作系统上，Python 的包逐渐被 Linux 的包管理器接管，例如，安装 pandas 可能需要 ``apt-get install python3-pandas`` 而非 ``python -m pip install pandas`` 或者 ``pip install pandas``（感觉还是以前比较方便且层次分明~~随后开始喜欢继续在 Windows 上运行 Python~~）。于是，执行 ``apt-get install python3-pip`` 并回车确认安装 pip。
继续 ``make test``，通过。
![make test](https://i-blog.csdnimg.cn/direct/73b35f94946d487db93d1cd735b130e5.png)
进入 Python，执行语句 ``from charm.toolbox.pairinggroup import PairingGroup, ZR, G1,G2, GT, pair``，没有报错或警告，即，导入成功。
![import](https://i-blog.csdnimg.cn/direct/f5a0ff7e58a7458d95e687a6ed3bae38.png)
至此，charm 环境部署成功。
# 附录
上述实验在以下两台设备中检验通过：
1) All the experiments conducted in this article are accomplished on 11th Gen Intel(R) Core(TM) i7-11800H CPU 2.30 GHz 8 cores, NVIDIA GeForce RTX 3060 Laptop GPU, 24 GB RAM, 512 GB SSD, and 1024 GB SSD under Windows 11 Pro 24H2 x64. The operating system is on the 512 GB SSD while the codes and the datasets are on the 1024 GB SSD. 
2) All the experiments conducted in this article are accomplished on the AMD Ryzen 7 7735H with Radeon Graphics (8 cores), 16 GB RAM, and 512 GB SSD under Windows 11 Pro 24H2 x64. 

准确一点，可能是：
1) All the experiments conducted in this article are accomplished on **the Ubuntu 24.04.1 LTS platform via the Windows subsystem for Linux (WSL) under** the 11th Gen Intel(R) Core(TM) i7-11800H CPU 2.30 GHz 8 cores, NVIDIA GeForce RTX 3060 Laptop GPU, 24 GB RAM, 512 GB SSD, and 1024 GB SSD under Windows 11 Pro 24H2 x64. The operating system is on the 512 GB SSD while the codes and the datasets are on the 1024 GB SSD. 
2) All the experiments conducted in this article are accomplished on **the Ubuntu 24.04.1 LTS platform via the Windows subsystem for Linux (WSL) under** the AMD Ryzen 7 7735H with Radeon Graphics (8 cores), 16 GB RAM, and 512 GB SSD under Windows 11 Pro 24H2 x64. 
