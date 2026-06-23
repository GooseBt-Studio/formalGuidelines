## Gaming

This directory stores some classic games and their save data. 

Only Chinese guidelines are provided in detail. 

---

## 游戏存档

此目录存储了一些经典的游戏及其存档。

### Windows

以下游戏已按游戏（集）发布时间升序排序，所有数据均保存在本地。除非有特别说明，下列游戏的安装包及其存档（如有）均已保存在本目录的子目录下。

- Windows XP 自带小游戏（请启动 [Windows XP 虚拟机](https://next.itellyou.cn/)进行游戏）
- [金山打字游戏](./Windows/金山打字游戏/)（金山打字通）
  - 生死时速(./Windows/金山打字游戏/dzt_great_race.exe)
  - 鼠的故事(./Windows/金山打字游戏/dzt_rat.exe)
  - 太空大战(./Windows/金山打字游戏/dzt_space_war.exe)
  - 拯救苹果(./Windows/金山打字游戏/dzt_apple.exe)
  - 激流勇进(./Windows/金山打字游戏/dzt_flume_ride.exe)
- [大鱼吃小鱼](./Windows/feeding_20100607.exe)
- [Flash 小游戏](./Windows/Flash/)
  - [EXE](./Windows/Flash/EXE/)：此目录保存了最新的 Flash Player（Flash Player 已于 2020 年 12 月 31 日停更）
  - [SWF](./Windows/Flash/SWF/)：此目录保存了一些经典的 Flash 小游戏
  - [SOL](./Windows/Flash/SOL/)：此目录保存了一些经典 Flash 小游戏的游戏存档（需要启动其对应的 ``*.swf`` 并通过 ``linkToGameArchives.bat`` 打开相应的目录后手动查找到真正的 ``.sol`` 文件进行替换才能生效）
  - [``linkToGameArchives.bat``](./Windows/Flash/linkToGameArchives.bat)
- [植物大战僵尸](./Windows/PlantsVsZombies/)
  - [程序](./Windows/PlantsVsZombies/Program.zip)
  - [一个可能的存档](./Windows/PlantsVsZombies/Archive.zip)
    - 在 Windows 7 及以上的操作系统中，解压后的两个文件夹应位于 ``C:\ProgramData\PopCap Games\PlantsVsZombies\`` 下
    - 在 Windows XP 中，解压后的两个文件夹应位于程序所在目录下
- [愤怒的小鸟](https://archive.org/download/angry-birds-pc/)（可使用 [``fetch.py``](./Windows/Rovio/fetch.py) 拉取）
  - 愤怒的小鸟原版
  - 愤怒的小鸟里约版
  - 愤怒的小鸟季节版
  - 愤怒的小鸟太空版（与手机版共用存档格式但手机版已无法在最新版安卓上运行）
  - 愤怒的小鸟星球大战版
  - 愤怒的小鸟星球大战版2
  - 捣蛋猪

对于愤怒的小鸟，可使用 [``gatherSaveData.py``](./Windows/Rovio/gatherSaveData.py) 将各路径上的存档保存在此目录下。

### Android

以下游戏已按游戏（集)发布时间升序排序，其中，保卫萝卜4、贪吃蛇大作战和奥比岛手游需要实时联网游戏；割绳子系列和开心消消乐的主线游戏可在离线模式下完成，但在完成后应当尽快提交到云端；
其余游戏均为单机游戏，但小部分过程（如中国大陆游戏登录时的实名认证、看广告领奖励和购买道具）可能仍需要联网。
所有单机游戏的所有本地数据均遵守安卓规则，不会向非应用数据目录写入数据；除需要实时联网的游戏外，用户可使用 Swift Backup 等备份还原软件进行备份和还原。
对于奥比岛手游，建议备份局部数据（Swift Backup 中的“数据”或 MT 管理器中的“数据目录1”）以避免清除数据或卸载重装后游戏内产生大量红点，同时避免产生占用空间较大的的备份文件。

本目录仅在本文档中提供部分游戏的下载链接，不存储任何安装包。此处，我们严厉抨击境内游戏分官服和渠道服的无良做法，并提供了一个 [``migrate.sh``](./Android/migrate.sh) 脚本以对单机游戏转服时进行数据迁移。

- 老人机经典游戏（暂未能保存）
  - 出人头地
  - 推箱子
  - 经典贪吃蛇
- 割绳子（数据均保存在本地但无法迁移）：请直接从 Play Store 安装
  - 割绳子 1：从谷歌商店安装
  - 割绳子 2：从谷歌商店安装（此为割绳子系列中最难的版本）
  - 割绳子之时空旅行：从谷歌商店安装
- [保卫萝卜](https://luobo.cn/)（所有版本均需要实名认证登录）
  - [保卫萝卜](https://luobo.737.com/1/android/)（保卫萝卜1）：官服（数据保存在本地；可以直接从官方下载安装包安装转为官服；转为官服后请在各渠道的软件商店屏蔽对该应用的更新）
  - [保卫萝卜2](https://luobo.737.com/2/android/)：官服（数据保存在本地）
  - [保卫萝卜3](https://luobo3.737.com/home/)：OPPO 渠道服
  - [保卫萝卜4](https://luobo4.737.com/)：华为渠道服
- [平衡球（HTC Teeter）](https://github.com/LRFP-Team/Teeter)
- [开心消消乐](https://kxxxl.leyuansu.com/)：官服
- [贪吃蛇大作战](https://www.tcsdzz.com/)：两个号均为 OPPO 渠道服
- [奥比岛手游](https://aobi.leiting.com/home)
  - [非官方指南](./Android/ObiIsland/)
  - 实验测试说明：一个号为官服、两个号为 OPPO 渠道服、一个号为华为渠道服
