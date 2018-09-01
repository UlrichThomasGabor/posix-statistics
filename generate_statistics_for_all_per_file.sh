#!/bin/bash
set -ue
cd "$(dirname "$0")"

cd statistics
for repos in *.posix; do
	repos="${repos%.*}"
	base="${repos##*.}"
	if [ "$base" = "5years" ] || [ "$base" = "10years" ]; then
		baserepos="${repos%.*}"
	else
		baserepos=repos
	fi
	../generate_statistics_per_file.py --posix_function_list ../posix_functions "$repos.posix" > "$repos.per_file"
done
