#!/usr/bin/env bash
INPUT=$@
DATE=${INPUT:-$(TZ="America/New_York" date +"%d")}
if test -d ${DATE}; then
    echo "${DATE} already exists"
    exit 1
fi

mkdir -p ${DATE}
cp template.py ${DATE}/solution.py
touch ${DATE}/__init__.py
touch ${DATE}/description.txt
touch ${DATE}/sample.txt
touch ${DATE}/input.txt
cp template.md ${DATE}/thoughts.md

cd ${DATE}
ln -s ../tools ./tools
