# Project: Reappropriation

# Author: Karandeep Singh Nagra


# Process notes files.  Create a Python dictionary for each entry.

# To call this script, execute:
# awk -f notes.awk ../all_notes.txt > notes_r.txt

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

    # Ignore empty lines
    if (match($0, /^$/)) {
        next
    }

    # Replace quotes with escaped quotes
    gsub(/"/, "\&quot;")

    # For whatever reason, tabs in the fourth entry also represent newlines.
    # So, append all entries after the fourth, separated by newline characters.
    if (NF > 4) {
        for (i = 5; i < NF; ++i) {
            $4 = $4 "<br />" $i
        }
    }

    print "{'timestamp': \"" $1 "\", 'name': \"" $2 "\", 'body': \"" $3 "\"}"
}
