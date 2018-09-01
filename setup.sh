#!/bin/bash
set -ue
cd "$(dirname "$0")"

echo "We are downloading a personal copy of the POSIX standard. Please note that these files are distributed with their own license!"
if [ ! -f susv4-2018.tgz ]; then
	echo "Downloading POSIX standard..."
	wget http://pubs.opengroup.org/onlinepubs/9699919799/download/susv4-2018.tgz
fi
if [ ! -d susv4-2018 ]; then
	echo "Extracting POSIX standard..."
	tar -xzf susv4-2018.tgz
fi
