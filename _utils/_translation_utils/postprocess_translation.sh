#!/bin/bash
# $1 is lang
# $2 is file
# sed -i 's/href=\"\//href=\"\/de\//g' de/pages/downloads.md
# actually for all the files in the pages directory

pattern="href=\"\/"
# TODO first reset with a regex group href=/($lang/).* (once or more vorhanden mit einfachen href=/
pattern_reset="href=\"\/"$1"\/"
pattern_replace="href=\"\/"$1"\/"
# find the patterns that contain href=/$lang pattern and reset
find $2 -name '*.md' -or -name '*.html' | xargs sed -i "s/$pattern_reset/$pattern/g"
find $2 -name '*.md' -or -name '*.html' | xargs sed -i "s/$pattern/$pattern_replace/g"
