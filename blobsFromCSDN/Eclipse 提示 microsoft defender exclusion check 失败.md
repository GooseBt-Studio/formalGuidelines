最近在新电脑上部署了 2024-06 版本的 Eclipse，导入原电脑的 Workstation 后打开提示 microsoft defender exclusion check 失败，原因为 failed to retrieve microsoft defender status。一种解决方案是降级（估计要到 2024-03 以下），一种方式是等待开发人员增强对 Microsoft Defender 状态的识别的鲁棒性（等更新）。如果不觉得 Defender 卡 Eclipse，可以试试本文的方法。

前往 [https://help.eclipse.org/latest/index.jsp?topic=%2Forg.eclipse.platform.doc.user%2Freference%2Fref-startup.htm](https://help.eclipse.org/latest/index.jsp?topic=%2Forg.eclipse.platform.doc.user%2Freference%2Fref-startup.htm) 查看可知，在菜单栏找到 Window，选择子菜单 Preferences，在弹出对话框中找到 General -> Startup and Shutdown，勾选 Skip exclusion check on startup for all new Eclipse-based installations 应用即可。
![Windows -> Preferences](https://i-blog.csdnimg.cn/direct/145e326fc0ab47088d1209d0b1df0d9e.png)
![skip checking](https://i-blog.csdnimg.cn/direct/a02b61a522e5439c99e8c15b9a820569.png)

