过环境检测，过完后玩游戏玩到手机没电，充上电一会之后忽然开不了机，系统自动重启进入恢复模式。由于手机会自动重启到恢复模式，所以应该还没有到达 fastboot 刷分区都无法解决的地步，也不是面具模块（一般导致的是 bootloop）导致的原因，于是进入恢复模式，输入手机密码后有个引导原因（第三方 Rec 会自动显示），内容如下，TWRP 还会告诉你解决方法是 清除缓存 或 格式化设备 或 clean-flash ROM。

```
android rescue party trigger! possible solutions?--reason=set_policy_failed:/data/local
```

于是找到 /data/local，里面只有一个 tmp 的空文件夹，问了下朋友，正常情况应该还有个 traces 文件夹，也是个空文件夹。于是启动临时 TWRP，建了个文件夹 traces 重启依旧不行。然后把 /data/local 及其子文件夹都赋值了 777 权限，重启依旧不行。最后的解决办法是，把整个 /data/local 删除重启就好了。开机后发现系统自己新建了 /data/local/tmp 和 /data/local/traces 两个空文件夹，据此推测估计是所有者不一致，所以自己新建文件夹无法修正错误。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/11b8c37a935643d8b923d90e9f90e120.jpeg)
系统自动创建的 /data/local 的所有者是 root，权限为 751，里面两个空的子文件夹的所有者是 shell，tmp 的权限是 771，traces 的权限是 777。据说，traces 是用来放系统跟踪日志的。

PS：以上修复过程不需要解密 data 分区（用户数据），只要使用的临时 TWRP 能够正常启动并完成对 /data/local 的修复即可。
