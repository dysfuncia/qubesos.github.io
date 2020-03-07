#!/bin/bash
# $1 is tx/config file
# $2 the new mapping file to be used by postprocess_translation.py
sed '/^$/d' $1 | sed '/source_lang/d' | sed '/^t/d' | sed '/^h/d' | sed '/\[main]/d' | sed '/\[/d'  > $2
