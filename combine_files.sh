#!/bin/sh

# Project: Reappropriation

# Author: Karandeep Singh Nagra

# Combine various files together for easier processing.
# Some of these files used integers primary keys;
# so each file has to be sectioned out with a line
# of form @@@<name_of_file> at the beginning.


# Remove files generate by old runs of this program first.
for i in all_food.txt all_maint.txt all_events.txt all_notes.txt
do
    if [ -e $1 ]
    then
        rm $i
    fi
done

# Food files
for i in food-2011.txt food-2012.txt food.txt
do
    echo "@@@$i" >> all_food.txt
    cat ../$i >> all_food.txt
done

# Maintenance files
for i in maintenance-2004.txt maintenance-2005.txt maintenance-2006.txt maintenance-2007.txt maintenance-2008.txt maintenance-2009.txt maintenance-2010.txt maintenance.txt
do
    echo "@@@$i" >> all_maint.txt
    cat ../$i >> all_maint.txt
done

# Events files
for i in events-2002.txt events-2003.txt events-2004.txt events-2005.txt events-2006.txt events-2007.txt events-2008.txt events-2009.txt events-2010.txt events.txt
do
    echo "@@@$i" >> all_events.txt
    cat ../$i >> all_events.txt
done

# Notes files
for i in notes-2002.txt notes-2003.txt notes-2004.txt notes-2005.txt notes-2006.txt notes-2007.txt notes-2008.txt notes-2009.txt notes-2010.txt notes-2011.txt notes-2012.txt notes-2013.txt notes.txt
do
    echo "@@@$i" >> all_notes.txt
    cat ../$i >> all_notes.txt
done
