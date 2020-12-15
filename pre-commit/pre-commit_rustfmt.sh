#!/bin/bash

for file in $(git diff --name-only --staged); do
    if [[ ${file} == *.rs ]]; then
		FMT_RESULT="$(rustfmt --edition=2018 $file 2>/dev/null)" # || true)"
    fi
done
