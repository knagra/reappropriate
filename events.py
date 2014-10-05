"""
Project: Reappropriation

Author: Karandeep Singh Nagra

Convert the processed output from all_events.txt using events.awk
into Django DB entries.
"""

from farnsworth.legacy.models import TeacherEvent

from .utils import read_dict, process_timestamp


def save_event(obj_dict, timestamp):
    """
    Create a TeacherEvent object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherEvent.
    timestamp should be a processed date object.
    """
    event = TeacherEvent(obj_dict)
    event.timestamp = timestamp
    event.save()

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
                    obj_dict.pop('date')
                    log_file_name,
                    "%Y-%m-%d"
                )
                if timestamp:
                    save_event(obj_dict, timestamp)
