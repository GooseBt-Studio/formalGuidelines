#!/usr/bin/bash

for mg in $(find /data -name "*io.github.vvb2060.magisk*")
do
	if [[ -e "${mg}" ]];
	then
		target=$(echo "${mg}" | sed 's/io.github.vvb2060.magisk/io.github.mmmmm/g')
		echo "\"${mg}\" -> \"${target}\""
		mv "${mg}" "${target}"
	fi
done