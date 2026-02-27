半年前从 Windows 10 升级到了 Windows 11，由于 Windows 隐藏了 Windows Defender 的任务栏图标，而笔者又用了火绒，故而没有及时注意到没有开启内核隔离。今天尝试开启内核隔离时，提示 passguard_64.sys 和 rtkvhd64.sys 导致无法开启内核隔离。关于 passguard_64.sys 的处理，网上教程特别多，这里就不多说了。不过笔者还是很好奇这个驱动是安装哪个程序时带上的，毕竟我把全部银联控件卸载了也不见它消失，重装最新版的控件回来也不见内核隔离能开启。

开始以为在设备管理器中右键让 Windows 更新声卡驱动就能解决，但提示已经是最新版，而实际上不是最新版。要处理 rtkvhd64.sys，只需要打开 Intel 官网 [https://www.intel.com/content/www/us/en/download/19455/realtek-high-definition-audio-driver-for-windows-10-64-bit-for-intel-nuc-kits-mini-pcs-nuc6cay.html](https://www.intel.com/content/www/us/en/download/19455/realtek-high-definition-audio-driver-for-windows-10-64-bit-for-intel-nuc-kits-mini-pcs-nuc6cay.html)，找到适用于 Windows 10、Windows 11 的最新版驱动包下载安装即可解决。当然，也可以用各种驱动管理软件更新或升级驱动。
![Intel](https://i-blog.csdnimg.cn/direct/848618adbdae4445bc93bbb1ec029fa2.png)

