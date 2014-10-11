#!/usr/bin/env python

"""
Project: Reappropriation

Author: Karandeep Singh Nagra

Execute main Python program.
"""


import sys, os

sys.path.append('/var/www/html/farnsworth')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farnsworth.settings")

from legacy import models

from utils import read_dict, process_timestamp


notes_added = 0


def save_note(obj_dict, timestamp):
    """
    Create a TeacherNote object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherNote.
    timestamp should be a processed datetime object.
    """
    note = models.TeacherNote(obj_dict)
    note.timestamp = timestamp
    note.save()
    global notes_added
    notes_added += 1
    print "Notes added: {}".format(notes_added)

def process_notes_file(file_name, log_file_name):
    """
    Process the file with name file_name, which contains dictionaries
    that describe TeacherNotes, one per line.
    """
    with open(file_name, 'r') as note_dicts:
        for line in note_dicts:
            obj_dict = read_dict(line, log_file_name)
            if obj_dict:
                timestamp = process_timestamp(
                    obj_dict.pop('timestamp'),
                    log_file_name,
                    "%Y-%m-%d %H:%M"
                )
                if timestamp:
                    save_note(obj_dict, timestamp)


events_added = 0


def save_event(obj_dict, timestamp):
    """
    Create a TeacherEvent object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherEvent.
    timestamp should be a processed date object.
    """
    event = models.TeacherEvent(obj_dict)
    event.timestamp = timestamp
    event.save()
    global events_added
    events_added += 1
    print "Events added: {}".format(events_added)

def process_events_file(file_name, log_file_name):
    """
    Process the file with name file_name, which contains dictionaries
    that describe TeacherEvents, one per line.
    """
    with open(file_name, 'r') as event_dicts:
        for line in event_dicts:
            obj_dict = read_dict(line, log_file_name)
            if obj_dict:
                timestamp = process_timestamp(
                    obj_dict.pop('date'),
                    log_file_name,
                    "%Y-%m-%d"
                )
                if timestamp:
                    save_event(obj_dict, timestamp)


requests_added = 0


def save_request(obj_dict, rtype, timestamp):
    """
    Create a TeacherRequest object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherRequest.
    rtype is the request type and should be either 'food' or 'maintenance'.
    timestamp should be a processed datetime object.
    """
    request = models.TeacherRequest(obj_dict)
    request.request_type = rtype
    request.timestamp = timestamp
    request.save()
    global requests_added
    requests_added += 1
    print "Requests added: {}".format(requests_added)


def save_response(obj_dict, rtype, timestamp):
    """
    Create a TeacherResponse object from the given dictionary.
    obj_dict should be of form {'teacher_key': tk, 'response': rdict},
    where rdict is a dictionary with all values necessary for
    generating a new TeacherResponse.
    rtype is the request type and should be either 'food' or 'maintenance'.
    timestamp should be a processed datetime object.
    """
    request = models.TeacherRequest.objects.get(
        teacher_key=obj_dict['teacher_key'],
        request_type = rtype
    )
    response = models.TeacherResponse(obj_dict['response'])
    response.request = request
    response.timestamp = timestamp
    response.save()


def process_requests_file(file_name, rtype, log_file_name):
    """
    Process the file with name file_name, which contains dictionaries
    that describe TeacherRequests and TeacherResponses, one per line.
    """
    with open(file_name, 'r') as request_dicts:
        for line in request_dicts:
            obj_dict = read_dict(line, log_file_name)
            if not obj_dict:
                continue    # read_dict failed and logged the error
            elif 'response' in obj_dict:
                timestamp = process_timestamp(
                    obj_dict['response'].pop('timestamp'),
                    log_file_name,
                    "%Y-%m-%d %H:%M"
                )
                if timestamp:
                    save_response(obj_dict, rtype, timestamp)
            else:
                timestamp = process_timestamp(
                    obj_dict.pop('timestamp'),
                    log_file_name,
                    "%Y-%m-%d %H:%M"
                )
                if timestamp:
                    save_request(obj_dict, rtype, timestamp)


def process_requests(food_file_name, maint_file_name, log_file_name):
    """
    Process all request files.
    """
    process_requests_file(food_file_name, 'food', log_file_name)
    process_requests_file(maint_file_name, 'maintenance', log_file_name)


def reappropriate(notes_file, events_file, food_file, maint_file):
    """Execute main Python program."""
    log_file_name = 'log.txt'
    print "Starting on notes...."
    process_notes_file(notes_file, log_file_name)
    print "Notes finished.  Starting on events...."
    process_events_file(events_file, log_file_name)
    print "Events finished.  Starting on requests...."
    process_requests(food_file, maint_file, log_file_name)
    print "Complete."


print "Starting Python script."

if __name__ == '__main__':
    print "Entered Python script."
    if len(sys.argv) != 5:
        print "Usage: ./main.py notes_file events_file food_file main_file"

    else:
        print "Processing args...."
        notes_file = sys.argv[1]
        events_file = sys.argv[2]
        food_file = sys.argv[3]
        maint_file = sys.argv[4]

        print "Done.  Starting reappropriation...."
        reappropriate(notes_file, events_file, food_file, maint_file)
