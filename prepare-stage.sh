#!/bin/bash

set -euo pipefail

stage="${1-}"

if [[ -z $stage ]]; then
	echo >&2 "Usage: $0 <stage>"
	exit
elif ! [[ $stage -ge 1 && $stage -le 5 ]]; then
	echo >&2 "Stage $stage is out of range [1, 5] or not a number."
	exit 1
elif ! git rev-parse --is-inside-work-tree &>/dev/null; then
	echo >&2 "This script must be run inside a git repository."
	exit 2
fi

if ! git diff-index --quiet HEAD -- 2>/dev/null; then
	read -rp "\
You have uncommitted changes and this script will OVERWRITE them.
Are you sure you want to continue?

Type 'yes' to continue: " confirm
	if [[ $confirm != yes ]]; then
		echo >&2 "Aborting."
		exit 3
	fi
fi

git clean -fdx
git restore -s origin/main .

seq 0 $((stage - 1)) | xargs -I '{}' git apply patches/stage-'{}'.patch
