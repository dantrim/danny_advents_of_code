#!/bin/bash

for file in $(git diff --name-only --staged); do
    if [[ ${file} == *.rs ]]; then
        "$(rustfmt --edition=2018 $file 2>/dev/null)" # || true)"
    fi
done
