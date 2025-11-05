#!/system/bin/sh
readonly EXIT_SUCCESS=0
readonly EXIT_FAILURE=1
exitCode=${EXIT_SUCCESS}
folders="/data/data /data/user/0 /data/user_de/0 /sdcard/Android/data"
packageNames="bin.mt.plus bin.mt.termex com.rifsxd.ksunext com.sukisu.ultra com.topjohnwu.magisk io.github.huskydg.magisk io.github.vvb2060.magisk me.bmax.apatch me.garfieldhan.apatch.next me.weishu.kernelsu"
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
