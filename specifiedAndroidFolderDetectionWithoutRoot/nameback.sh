#!/usr/bin/bash

for mg in $(find /data -name "*io.github.mmmmm*")
do
	if [[ -e "${mg}" ]];
	then
		target=$(echo "${mg}" | sed 's/io.github.mmmmm/io.github.vvb2060.magisk/g')
		echo "\"${mg}\" -> \"${target}\""
		mv "${mg}" "${target}"
	fi
done