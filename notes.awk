#!/usr/bin/awk -f

# Project: Reappropriation

# Author: Karandeep Singh Nagra


# Process notes files.  Create a Python dictionary for each entry.

# To call this script, execute:
# ./notes.awk ../all_notes.txt > notes_r.txt

# Set the field separator to the tab character
# This will make the fields:
# $1 := time stamp
# $2 := user-provided name
# $3 := note body
# possibly $(>=5) := extra lines of the body
BEGIN {
    FS = "\t"
}

{
    # Section head
    if (match($0, /^@@@/)) {
        ++section_number
        next
    }

    if (match($0, /^$/)) {
        next
    }

    gsub(/^# */, "", $0)

    gsub(/made me cry. :\\/, "made me cry. :\\\\", $0)

    gsub(/"/, "\&quot;")

    # For whatever reason, tabs in the fourth entry also represent newlines.
    # So, append all entries after the fourth, separated by newline characters.
    if (NF > 3) {
        for (i = 4; i < NF; ++i) {
            $3 = $3 "<br />" $i
        }
    }

    if (match($0, /ORANGEE/)) {
        getline truncated_line
        $3 = substr($3,0,25) substr(truncated_line,2)
    }

    print "{'timestamp': \"" $1 "\", 'name': \"" $2 "\", 'body': \"" $3 "\"}"
}
