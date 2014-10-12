#!/usr/bin/env python

"""
Project: Reappropriation

Author: Karandeep Singh Nagra

Execute main Python program.
"""


import sys, os
from multiprocessing import Process


import ast
from datetime import datetime

import django
from django.utils.timezone import utc


def to_unicode(obj_dict):
    """Convert relevant elements of the dictionary to unicode."""
    for key in obj_dict:
        if key != 'timestamp' and key != 'date' and key != 'response':
            if len(obj_dict[key]) > 0 and obj_dict[key][-1] == "\\":
                obj_dict[key] = unicode(obj_dict[key][:-2], 'utf-8', 'replace')
                obj_dict[key] += '\\'
            else:
                obj_dict[key] = unicode(obj_dict[key], 'utf-8', 'replace')
        elif key == 'response':
            obj_dict[key] = to_unicode(obj_dict[key])
    return obj_dict


def read_dict(line, log_file_name):
    """
    Interpret a string as a dict.
    If it fails, log it and move on.
    Return the dictionary if it was processed properly, False otherwise.
    """
    try:
        return to_unicode(ast.literal_eval(line))
    except ValueError as e:
        with open(log_file_name, 'a') as log_file:
            log_file.write(
                '[VALUE ERROR] Read_dict failed on the following line: {line}\n'.format(
                    line=line
                )
            )
            log_file.write('\tError message: {error}'.format(error=e))
            log_file.write('\n\n')
        return False
    except SyntaxError as e:
        with open(log_file_name, 'a') as log_file:
            log_file.write(
                '[SYNTAX ERROR] Read_dict failed on following line: {line}\n'.format(
                    line=line
                )
            )
            log_file.write('\tError message: {error}'.format(error=e))
            log_file.write('\n\n')
        return False


def process_timestamp(string, log_file_name, fmt='datetime'):
    """
    Create a datetime object timestamp from the legacy string,
    which is of format fmt.
    """
    try:
        return datetime.strptime(string, fmt).replace(tzinfo=utc)
    except ValueError as e:
        with open(log_file_name, 'a') as log_file:
            log_file.write(
                '[VALUE ERROR] Process_timestamp failed on: {string}\n'.format(
                    string=string
                ))
            log_file.write('\tError message: {error}'.format(error=e))
            log_file.write('\n\n')
        return False


def create_note(obj_dict, timestamp):
    """
    Create a TeacherNote object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherNote.
    timestamp should be a processed datetime object.
    Return the created note object.
    """
    return models.TeacherNote(
        name=obj_dict['name'],
        body=obj_dict['body'],
        timestamp=timestamp,
    )

def process_notes_file(file_name, log_file_name):
    """
    Process the file with name file_name, which contains dictionaries
    that describe TeacherNotes, one per line.
    """
    with open(file_name, 'r') as note_dicts:
        notes = []
        line_count = 0
        for line in note_dicts:
            line_count += 1
            obj_dict = read_dict(line, log_file_name)
            if obj_dict:
                timestamp = process_timestamp(
                    obj_dict.pop('timestamp'),
                    log_file_name,
                    "%Y-%m-%d %H:%M"
                )
                if timestamp:
                    notes.append(create_note(obj_dict, timestamp))
    if notes:
        models.TeacherNote.objects.bulk_create(notes)
    print "\tAdded {}/{} notes.".format(len(notes), line_count)


def create_event(obj_dict, timestamp):
    """
    Create a TeacherEvent object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherEvent.
    timestamp should be a processed date object.
    Return the created event.
    """
    return models.TeacherEvent(
        date=timestamp,
        title=obj_dict['title'],
        description=obj_dict['description'],
    )

def process_events_file(file_name, log_file_name):
    """
    Process the file with name file_name, which contains dictionaries
    that describe TeacherEvents, one per line.
    """
    with open(file_name, 'r') as event_dicts:
        events = []
        line_count = 0
        for line in event_dicts:
            line_count += 1
            obj_dict = read_dict(line, log_file_name)
            if obj_dict:
                timestamp = process_timestamp(
                    obj_dict.pop('date'),
                    log_file_name,
                    "%Y-%m-%d"
                )
                if timestamp:
                    events.append(create_event(obj_dict, timestamp))
    if events:
        models.TeacherEvent.objects.bulk_create(events)
    print "\tAdded {}/{} events.".format(len(events), line_count)


def create_request(obj_dict, rtype, timestamp):
    """
    Create a TeacherRequest object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherRequest.
    rtype is the request type and should be either 'food' or 'maintenance'.
    timestamp should be a processed datetime object.
    Return the created request.
    """
    return models.TeacherRequest(
        teacher_key=obj_dict['teacher_key'],
        timestamp=timestamp,
        name=obj_dict['name'],
        body=obj_dict['body'],
        request_type=rtype,
    )


def create_response(obj_dict, rtype, timestamp, log_file_name):
    """
    Create a TeacherResponse object from the given dictionary.
    obj_dict should be of form {'teacher_key': tk, 'response': rdict},
    where rdict is a dictionary with all values necessary for
    generating a new TeacherResponse.
    rtype is the request type and should be either 'food' or 'maintenance'.
    timestamp should be a processed datetime object.
    Return the created response.
    """
    try:
        request = models.TeacherRequest.objects.get(
            teacher_key=obj_dict['teacher_key'],
            request_type=rtype,
        )

    except models.TeacherRequest.DoesNotExist:
        try:
            teacher_suffix = int(obj_dict['teacher_key'][-1]) - 1
            teacher_key = obj_dict['teacher_key'][:-1] + str(teacher_suffix)
            request = models.TeacherRequest.objects.get(
                teacher_key=teacher_key,
                request_type=rtype,
            )

        except models.TeacherRequest.DoesNotExist as e:
            with open(log_file_name, 'a') as log_file:
                log_file.write(
                    '[DOES NOT EXIST] Could not find request for following response dict: {dict}\n'\
                    .format(
                        dict=obj_dict
                    )
                )
                log_file.write('Error message: {error}'.format(error=e))
                log_file.write('\n\n')
            return False

        else:
            response_dict = obj_dict['response']
            return models.TeacherResponse(
                request=request,
                name=response_dict['name'],
                body=response_dict['body'],
                timestamp=timestamp,
            )

    else:
        response_dict = obj_dict['response']
        return models.TeacherResponse(
            request=request,
            name=response_dict['name'],
            body=response_dict['body'],
            timestamp=timestamp,
        )


def add_all_requests(requests, log_file_name, rtype):
    """Add all requests in the list requests."""
    request_objects = []
    for request_dict in requests:
        timestamp = process_timestamp(
            request_dict.pop('timestamp'),
            log_file_name,
            "%Y-%m-%d %H:%M",
        )

        if timestamp:
            request_object = create_request(request_dict, rtype, timestamp)
            if request_object:
                request_objects.append(request_object)

    models.TeacherRequest.objects.bulk_create(request_objects)

    print "\tAdded {}/{} {} requests.".format(
        len(request_objects),
        len(requests),
        rtype,
    )


def add_all_responses(responses, log_file_name, rtype):
    """Add all responses in the list responses."""
    response_objects = []

    for response_dict in responses:
        timestamp = process_timestamp(
            response_dict['response'].pop('timestamp'),
            log_file_name,
            "%Y-%m-%d %H:%M",
        )

        if timestamp:
            response_object = create_response(
                response_dict, rtype, timestamp, log_file_name
            )
            if response_object:
                response_objects.append(response_object)

        else:
            with open(log_file_name, 'a') as log_file:
                log_file.write(
                    'Could not find process timestamp for response dict: {dict}\n'\
                    .format(
                        dict=response_dict
                    )
                )
                log_file.write('\n\n')
            return False

    models.TeacherResponse.objects.bulk_create(response_objects)

    print "\tAdded {}/{} {} responses.".format(
        len(response_objects),
        len(responses),
        rtype,
    )


def process_requests_file(file_name, rtype, log_file_name):
    """
    Process the file with name file_name, which contains dictionaries
    that describe TeacherRequests and TeacherResponses, one per line.
    """
    with open(file_name, 'r') as request_dicts:
        responses = []
        requests = []

        responses_added = 0
        requests_added = 0

        for line in request_dicts:
            obj_dict = read_dict(line, log_file_name)

            if not obj_dict:
                continue    # read_dict failed and logged the error

            elif 'response' in obj_dict:
                responses.append(obj_dict)

            else:
                requests.append(obj_dict)

    add_all_requests(requests, log_file_name, rtype)
    add_all_responses(responses, log_file_name, rtype)


def process_requests(food_file_name, maint_file_name, log_file_name):
    """
    Process all request files.
    """
    process_requests_file(food_file_name, 'food', log_file_name)
    process_requests_file(maint_file_name, 'maintenance', log_file_name)

def reappropriate(notes_file, events_file, food_file, maint_file):
    """Execute main Python program."""
    log_file_name = 'log.txt'
    print "Initializing Django"
    django.setup()

    print "Starting legacy tables clean...."
    models.TeacherNote.objects.all().delete()
    models.TeacherEvent.objects.all().delete()
    models.TeacherResponse.objects.all().delete()
    models.TeacherRequest.objects.all().delete()

    print "Done.  Populating database with new objects"

    add_notes_process = Process(
        target=process_notes_file,
        args=(notes_file, log_file_name,),
    )
    add_events_process = Process(
        target=process_events_file,
        args=(events_file, log_file_name,),
    )
    add_requests_process = Process(
        target=process_requests,
        args=(food_file, maint_file, log_file_name,),
    )

    add_notes_process.start()
    add_events_process.start()
    add_requests_process.start()

    for proc in (add_notes_process, add_events_process, add_requests_process):
        proc.join()
        proc.terminate()

    print "Reappropriation complete."


print "Starting Python script."

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print "Usage: ./main.py notes_file events_file food_file main_file"

    else:
        notes_file = sys.argv[1]
        events_file = sys.argv[2]
        food_file = sys.argv[3]
        maint_file = sys.argv[4]
        farnsworth_dir = sys.argv[5]

        sys.path.append(farnsworth_dir)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farnsworth.settings")

        from legacy import models

        print "Starting reappropriation...."
        reappropriate(notes_file, events_file, food_file, maint_file)
