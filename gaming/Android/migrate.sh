#!/system/bin/sh
readonly EXIT_SUCCESS=0
readonly EXIT_FAILURE=1
readonly EOF=-1

# Input Parameters #
readonly sourcePackageName="com.feiyu.carrot3.nearme.gamecenter"
readonly targetPackageName="com.feiyu.carrot3"
readonly sourceHash="5b7e993a36ee87a428198964b4bf2d04"
readonly targetHash="935ed64f246852ba2e4c34e8dd09e6b7"
readonly sourceLibCode="058881d9.so"
readonly targetLibCode="4371f174.so"
readonly sourceCookie="30563.yaqcookie"
readonly targetCookie="15098.yaqcookie"
readonly timeout=5

# Information Gathered #
sourceFolderPath="/data/user/0/${sourcePackageName}"
targetFolderPath="/data/user/0/${targetPackageName}"
if [[ ! -d "${sourceFolderPath}" ]];
then
	echo "Error: The source folder \"${sourceFolderPath}\" does not exist. Please make sure that you have installed \`\`${sourcePackageName}\`\`. "
	exit ${EOF}
fi
if [[ -d "${targetFolderPath}" ]];
then
	targetUID="$(ls -ld ${targetFolderPath} | cut -d ' ' -f3)"
	echo "Info: Gathered target UID ${targetUID} for \`\`${targetPackageName}\`\`. "
else
	echo "Error: The target folder \"${targetFolderPath}\" does not exist. Please make sure that you have installed \`\`${targetPackageName}\`\`. "
	exit ${EOF}
fi

# Operation Confirmation #
echo "This script will attempt to migrate data from \`\`${sourcePackageName}\`\` to \`\`${targetPackageName}\`\`. Please check the code and acknowledge the risk on your own. "
echo -n "This script will remove all the data under the folder \"${targetFolderPath}\" if any before migrating. Continue or not? [yN] "
read toBeConfirmed
if [[ $? -ne 0 ]];
then
	echo "Users did not response in ${timeout} second(s). "
	exit ${EOF}
fi
if [[ "${toBeConfirmed}" == "Y" || "${toBeConfirmed}" == "y" ]];
then
	echo "Users have acknowledged the potential risks and confirmed the operation. "
else
	echo "Users cancelled the operation. "
	exit ${EXIT_SUCCESS}
fi

# Execution #
if [[ -n "${targetFolderPath}" && "${targetFolderPath}" != "/data" && "${targetFolderPath}" != "/data/user" && "${targetFolderPath}" != "/data/user/0" && "${targetFolderPath}" != "/sdcard" ]];
then
	exitCode=${EXIT_SUCCESS}
	if ! rm -rf "${targetFolderPath}"/*;
	then
		echo "Warning: Failed to clear the target folder \"${targetFolderPath}\". "
		exitCode=${EXIT_FAILURE}
	fi
	find "${sourceFolderPath}" -type f | while read -r sourceFilePath;
	do
		relativePath="${sourceFilePath#$sourceFolderPath/}"
		targetFilePath=$(echo "${targetFolderPath}/${relativePath}" | sed "s/${sourceHash}/${targetHash}/g" | sed "s/${sourceLibCode}$/{targetLibCode}/g" | sed "s/${sourceCookie}/${targetCookie}/g")
		targetFileParentPath="$(dirname "${targetFilePath}")"
		mkdir -p "${targetFileParentPath}" && cp "${sourceFilePath}" "${targetFilePath}"
		returnCode=$?
		if [[ ${returnCode} -eq ${EXIT_SUCCESS} ]];
		then
			echo "[V] \"${sourceFilePath}\" -> \"${targetFilePath}\" (${returnCode})"
		else
			echo "[!] \"${sourceFilePath}\" -> \"${targetFilePath}\" (${returnCode})"
			exitCode=${EXIT_FAILURE}
		fi
	done
	if chown -R ${targetUID}:${targetUID} "${targetFolderPath}";
	then
		echo "Successfully changed the owner and the user group to ${targetUID}. "
	else
		echo "Failed to change the owner and the user group to ${targetUID}. "
		exitCode=${EXIT_FAILURE}
	fi
	exit ${exitCode}
else
	echo "Fatal: The target folder path has been maliciously modified to \"/\". "
	exit ${EOF}
fi
