#!/bin/sh

# Project: Reappropriation

# Author: Karandeep Singh Nagra

# Run the whole program

./combine_files.sh

./notes.awk all_notes.txt > notes_r.txt
./events.awk all_events.txt > events_r.txt
./requests.awk all_food.txt > food_r.txt
./requests.awk all_maint.txt > maint_r.txt

./main.py notes_r.txt events_r.txt food_r.txt maint_r.txt
