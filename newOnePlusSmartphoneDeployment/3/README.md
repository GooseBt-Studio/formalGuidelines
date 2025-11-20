### 切换为 Sun OS

在阅读本文档前，请先知晓 Sun OS（原名为“Nameless OS”）是第三方 ROM，接近于原生安卓系统；此处，笔者仅建议使用一加 13 系列的用户切换其手机操作系统为 Sun OS，原因如下。

1) 对于官方出厂搭载氢系统的一加手机（例如一加 7 Pro）：使用氢系统是非常完美的选择，因为氢系统是一加手机所有官方出厂搭载的系统中的巅峰。
2) 对于官方出厂搭载安卓 11 以及下版本的氧系统的一加手机（例如一加 9 Pro）：保持使用安卓 11 中最新的氧系统是非常完美的选择，因为自安卓 12 开始氧系统就是套了皮的 Color OS 系统，并不（类）原生。
3) 其它：可以考虑切换为自定义 ROM，但从一加 10 开始，一加官方不再开放救砖包，用户只能前往售后服务中心进行免费救砖，或在某些平台上付费远程救砖，而目前 Sun OS 的 Super Flashers 仅适配了一加 13 系列。
此处，笔者不推荐使用自己刷入第三方 ROM 的原因是，切换第三方系统需要梳理出各种切换关系（例如需要先切去低版本的 Oxygen OS 再切去低版本的第三方 ROM 再升级）和各种锁（其中一些会让手机“黑砖”），
并面对更复杂的分区环境，容易让手机变砖，而没有开放的救砖包，救砖就会变得很麻烦，用户尝试的成本就会大幅度升高。因此，即使一加手机上没有任何数据，也要谨慎操作！
此处，强烈建议完全开放 BootLoader 解锁的手机设备厂商开放救砖包以减轻售后服务负担，并能够减少黑灰产业链的滋生。

如不需要切换 Sun OS，请返回上级目录。

根据[上一篇文档](../2/README.md)中的指引再次处理开发者模式，使得已连接个人电脑且已解除屏幕锁定的手机能够被个人电脑的 ``adb.exe`` 识别（适当目录下执行 ``adb devices`` 命令后得到一个序列号和 ``device``）。

在一台能够科学上网的个人电脑上访问 [https://www.nameless.wiki/getting-started/supported-devices](https://www.nameless.wiki/getting-started/supported-devices) 以查看支持的设备，
确保自己的一加手机被 Nameless 官方支持。

~~随后，根据[官方指引](https://www.nameless.wiki/getting-started/flash-instructions) 完成操作即可。这样大概率会让设备黑砖！~~

随后，前往 [https://roms.danielspringer.at/index.php?dir=Oneplus+13%2FCustom+Roms%2FSunOS+Super+Flashers](https://roms.danielspringer.at/index.php?dir=Oneplus+13%2FCustom+Roms%2FSunOS+Super+Flashers)，
在一台 64 位的 Windows 10 或 Windows 11 上选择一个最新版本的 Sun OS 下载，解压后，以管理员权限启动解压后根目录中的 ``SUPERHYBRID_SUNOS_FLASHER.bat`` 文件，根据指引完成操作即可。
