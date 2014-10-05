"""
Project: Reappropriation

Author: Karandeep Singh Nagra

Convert the processed output from all_notes.txt using notes.awk
into Django DB entries.
"""

from farnsworth.legacy.models import TeacherNote

from .utils import read_dict, process_timestamp


def save_note(obj_dict, timestamp):
    """
    Create a TeacherNote object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherNote.
    timestamp should be a processed datetime object.
    """
    note = TeacherNote(obj_dict)
    note.timestamp = timestamp
    note.save()

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
