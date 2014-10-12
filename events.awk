#!/usr/bin/awk -f

# Project: Reappropriation

# Author: Karandeep Singh Nagra


# Process events files.  Create a Python dictionary for each entry.

# To call this script, execute:
# ./events.awk ../all_events.txt > events_r.txt

# Set the field separator to the tab character
# This will make the fields:
# $2 := date of event
# $3 := title of event
# $4 := event description
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

    gsub(/"/, "\&quot;")

    # For whatever reason, tabs in the fourth entry also represent newlines.
    # So, append all entries after the fourth, separated by newline characters.
    if (NF > 3) {
        for (i = 4; i < NF; ++i) {
            $3 = $3 "<br />" $i
        }
    }

    print "{'date': \"" $1 "\", 'title': \"" $2 "\", 'description': \"" $3 "\"}"
}
