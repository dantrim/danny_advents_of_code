#!/bin/bash

for file in $(git diff --name-only --staged); do
    if [[ ${file} == *.rs ]]; then
        FMT_RESULT="$(rustfmt --edition=2018 $file 2>/dev/null)" # || true)"
        if [ "$FMT_RESULT" != "" ]; then
            if [ $FIRST_FILE -eq 0 ]; then
                echo -n ", "
            fi  
        fi
    fi
done
