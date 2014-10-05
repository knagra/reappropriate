# Project: Reappropriation

# Author: Karandeep Singh Nagra


# Process requests files.  Create a Python dictionary for each entry.

# To call this script, execute:
# awk -f food.awk ../all_food.txt > food_r.txt

# Set the field separator to the tab character
# This will make the fields:
# $1 := time-stamp-based primary key, starts with > if a response
# $2 := time stamp
# $3 := user-provided name
# $4 := request/response body
# possibly $(>=5) := extra lines of the body
BEGIN {
    FS = "\t"
    section_number = 1
}

{
    # If it's a section head, increment the section_number and move on
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

    # If the record begins the > character, it's a response to the request
    # with $1[2:] as the primary key
    if ($1 ~ "^>") {
        print "{'teacher_key': \"" substr($1,2) "_" section_number "\", 'response': {'timestamp': \"" $2 "\", 'name': \"" $3 "\", 'body': \"" $4 "\"}}"
        next
    }

    print "{'teacher_key': \"" $1 "_" section_number "\", 'timestamp': \"" $2 "\", 'name': \"" $3 "\", 'body': \"" $4 "\"}"
}
