#!/bin/bash
set -ue
cd "$(dirname "$0")"

cd repositories
statistics="../statistics"

mkdir -p "$statistics"

for repos in */; do
	repos=${repos%?}
	echo "Computing posix-count for $repos"
	if [ ! -f "$statistics/$repos.posix" ]; then
		grep -REhIoe "$(cut -f3 ../posix_functions)" --include="*.h" --include="*.hpp" --include="*.c" --include="*.cc" --include="*.cpp" --include="*.cxx" "$repos"|cut -d"(" -f1|awk '{$1=$1};1'|sort|uniq -c > "$statistics/$repos.posix"
	else
		echo "$statistics/$repos.posix exists; skipping"
	fi

	oldbranch=$(cd "$repos" && git rev-parse --abbrev-ref HEAD)
	echo "Remembered $oldbranch for later checkout"

	echo "Computing 5-years ago posix for $repos"
	fiveyearbranch=$(cd "$repos" && git rev-list -n 1 --before="2013-08-20 00:00" HEAD)
	if [ -n "$fiveyearbranch" ]; then
		if [ ! -f "$statistics/$repos.5years.posix" ]; then
			$(cd "$repos" && git checkout "$fiveyearbranch")
			grep -REhIoe "$(cut -f3 ../posix_functions)" --include="*.h" --include="*.hpp" --include="*.c" --include="*.cc" --include="*.cpp" --include="*.cxx" "$repos"|cut -d"(" -f1|awk '{$1=$1};1'|sort|uniq -c > "$statistics/$repos.5years.posix"
		else
			echo "$statistics/$repos.5years.posix exists; skipping"
		fi
	else
		echo "No commit from 5 years ago."
	fi

	echo "Computing 10-years ago posix for $repos"
	tenyearbranch=$(cd "$repos" && git rev-list -n 1 --before="2008-08-20 00:00" HEAD)
	if [ -n "$tenyearbranch" ]; then
		if [ ! -f "$statistics/$repos.10years.posix" ]; then
			$(cd "$repos" && git checkout "$tenyearbranch")
			grep -REhIoe "$(cut -f3 ../posix_functions)" --include="*.h" --include="*.hpp" --include="*.c" --include="*.cc" --include="*.cpp" --include="*.cxx" "$repos"|cut -d"(" -f1|awk '{$1=$1};1'|sort|uniq -c > "$statistics/$repos.10years.posix"
		else
			echo "$statistics/$repos.10years.posix exists; skipping"
		fi
	else
		echo "No commit from 10 years ago."
	fi

	cd "$repos"
	git checkout "$oldbranch"
	cd ..
done
