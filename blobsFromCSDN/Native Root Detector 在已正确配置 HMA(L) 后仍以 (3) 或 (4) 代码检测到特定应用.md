本文将大致介绍一下 Native Root Detector 在已正确配置 HMA(L) 后仍以 (3) 或 (4) 代码检测到特定应用的原理，主要是困扰了很久，在谷歌和百度都查不到，现在知道了，发出来分享。

代码 (4)，其实就是检测到了特定目录下存在以特定包名命名的文件夹，例如 /sdcard/Android/data/io.github.vvb2060.magisk。该目录在部分安卓系统上不需要 root 权限也可以被判定存在，即使无法进行写入或执行 ``ls`` 命令。如果是空文件夹，删除即可。有兴趣的读者朋友可以使用 MT 管理器在非 root 模式下执行以下脚本来检测是否存在目录泄露的情况。

```
#!/system/bin/sh
readonly EXIT_SUCCESS=0
readonly EXIT_FAILURE=1
exitCode=${EXIT_SUCCESS}
folders="/data/data /data/user/0 /data/user_de/0 /sdcard/Android/data"
packageNames="com.rifsxd.ksunext com.sukisu.ultra com.topjohnwu.magisk io.github.huskydg.magisk io.github.vvb2060.magisk me.bmax.apatch me.garfieldhan.apatch.next me.weishu.kernelsu"
for packageName in ${packageNames}
do
	for folder in ${folders}
	do
		if [[ -e "${folder}/${packageName}" ]];
		then
			exitCode=${EXIT_FAILURE}
			echo "Found \"${folder}/${packageName}\". "
		fi
	done
done
exit ${exitCode}
```

代码 (3) 对应的检测适用于安卓 13 以下的操作系统，通过启动目标应用的 Activity 实现检测，已于 2025 年 6 月 25 日在 ``HMA_v3.5.r449.1d951a3 (449)`` 中得到修复。

![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/331f39760dab4b62a0349d90191f1cce.png)


