#!/bin/bash

HAS_ISSUES=0
FIRST_FILE=1

echo "DOOBLY"
for file in $(git diff --name-only --staged); do
    #FMT_RESULT="$(rustfmt --skip-children --force --write-mode diff $file 2>/dev/null || true)"
    FMT_RESULT="$(rustfmt --edition=2018 $file 2>/dev/null || true)"
    echo "FOOBLY"
    if [ "$FMT_RESULT" != "" ]; then
        if [ $FIRST_FILE -eq 0 ]; then
            echo -n ", "
        fi  
        echo -n "$file"
        HAS_ISSUES=1
        FIRST_FILE=0
    fi
done

if [ $HAS_ISSUES -eq 0 ]; then
    exit 0
fi

echo ". Your code has formatting issues in files listed above. Format your code with \`make format\` or call rustfmt manually."
exit 1
