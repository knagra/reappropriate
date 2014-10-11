#!/bin/sh

# Project: Reappropriation

# Author: Karandeep Singh Nagra

# Run the whole program

echo "Combining files...."
./combine_files.sh

echo "Done.  Processing notes...."
./notes.awk all_notes.txt > notes_r.txt
echo "Done.  Processing events...."
./events.awk all_events.txt > events_r.txt
echo "Done.  Processing food requests...."
./requests.awk all_food.txt > food_r.txt
echo "Done.  Processing maintenance requests...."
./requests.awk all_maint.txt > maint_r.txt

echo "Done.  Adding Django DB entries...."
./main.py notes_r.txt events_r.txt food_r.txt maint_r.txt
