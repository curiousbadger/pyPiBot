#!/bin/bash
# say() { local IFS=+;/usr/bin/mplayer -noconsolecontrols "http://translate.google.com/translate_tts?tl=en&q=$*"; }
# say $*

echo "$*" | festival --tts