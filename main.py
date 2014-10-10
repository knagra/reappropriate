#!/usr/bin/env python

"""
Project: Reappropriation

Author: Karandeep Singh Nagra

Execute main Python program.
"""

import sys

from notes import process_notes_file
from events import process_events_file
from requests import process_requests


def reappropriate(notes_file, events_file, food_file, maint_file):
    """Execute main Python program."""
    log_file_name = 'log.txt'
    process_notes_file(notes_file, log_file_name)
    process_events_file(events_file, log_file_name)
    process_requests(food_file, maint_file, log_file_name)


if __name__ == 'main':
    if len(sys.argv) != 5:
        print "Usage: ./main.py notes_file events_file food_file main_file"

    notes_file = sys.argv[1]
    events_file = sys.argv[2]
    food_file = sys.argv[3]
    maint_file = sys.argv[4]

    reappropriate(notes_file, events_file, food_file, maint_file)
