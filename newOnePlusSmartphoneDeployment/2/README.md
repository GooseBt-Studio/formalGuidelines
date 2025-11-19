### 解锁 BootLoader

在阅读本文档前，请先知晓解锁 BootLoader 会**清除手机上的所有数据**，解锁 BootLoader 后的手机将存在一定的数据泄露风险！请读者朋友们确认清楚自己在做什么再继续往下阅读文档！

打开设置，点击“关于本机”，点击“版本信息”，连续 5 次点击“版本号”；此时，系统会显示一条弹出式通知，大约内容为“您现在处于开发者模式！”或“您已处于开发者模式，无需进行此操作。”。

连续点击返回直至返回设置主页面，点击“系统与更新”，点击“开发者选项”，打开 USB 调试和 OEM 解锁。

在一台能够科学上网的个人电脑上访问[安卓调试桥](https://developer.android.com/tools/releases/platform-tools/)并下载使用于当前个人电脑平台的最新安卓平台 SDK。
将下载后的工具解压到 ``C:\Android``（此处以 ``C:\Android`` 为例）下，使得 ``adb.exe`` 和 ``fastboot.exe`` 的路径分别为 ``C:\Android\adb.exe`` 和 ``C:\Android\fastboot.exe``。

在个人电脑中按下“Win + R”组合快捷键（其中“Win”键是位于键盘左侧 Ctrl 和 Alt 之间的 Windows 徽标），在弹出对话框中键入 cmd，回车；
在弹出的 cmd 窗口中键入 ``cd C:\Android`` 并回车进入 ``C:\Android``。如有能力或有长期需求也可以将 ``C:\Android`` 目录加入系统环境变量 PATH 中以免除 ``cd`` 步骤。

将个人电脑和一加手机通过一条优质的数据线（例如原装充电器的数据线）连接（不建议同时连接其它安卓设备），
解除手机的屏幕锁定并在手机屏幕再次锁定前在个人电脑的上述 cmd 窗口中输入 ``adb devices`` 并回车，如手机询问是否允许调试则授权。
再次在个人电脑的上述 cmd 窗口中输入 ``adb devices`` 并回车，此时在 cmd 窗口中将显示一个序列号和 ``device``；继续键入 ``adb reboot bootloader`` 并回车，等待手机重启并进入 fastboot 模式；
继续键入 ``fastboot flashing unlock``（部分旧机型的命令为 ``fastboot oem unlock``）回车，此时手机进入 BootLoader 解锁确认界面，操作手机的音量键盘使得 ``UNLOCK THE BOOTLOADER``被高亮，按下电源键，
此时手机将解锁 BootLoader 并**清除手机上的所有数据**，随后重启进入系统。

此时，BootLoader 解锁完成。
