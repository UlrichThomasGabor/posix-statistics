#!/bin/bash
set -ue
cd "$(dirname "$0")"

mkdir -p repositories

sort $@|uniq | while read line
do
	if [ ! -z "$line" ]; then
		echo "Cloning $line"
		cd repositories
		git clone "$line.git" $(echo "$line" | cut -d/ -f4,5 | tr "/" "_")
		cd ..
	fi
done
