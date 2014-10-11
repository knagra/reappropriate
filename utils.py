"""
Project: Reappropriation

Author: Karandeep Singh Nagra

Utilities used elsewhere in this program.
"""


import ast
from datetime import datetime


def read_dict(line, log_file_name):
    """
    Interpret a string as a dict.
    If it fails, log it and move on.
    Return the dictionary if it was processed properly, False otherwise.
    """
    try:
        return ast.literal_eval(line)
    except ValueError as e:
        with open(log_file_name, 'a') as log_file:
            log_file.write(
                'Read_dict failed on following line: {line}'.format(
                    line=line
                ))
            log_file.write('Error message: {error}'.format(error=e))
        return False

def process_timestamp(string, log_file_name, fmt='datetime'):
    """
    Create a datetime object timestamp from the legacy string,
    which is of format fmt.
    """
    try:
        return datetime.strptime(string, fmt)
    except ValueError as e:
        with open(log_file_name, 'a') as log_file:
            log_file.write(
                'process_timestamp failed on: {string}'.format(
                    string=string
                ))
            log_file.write('Error message: {error}'.format(error=e))
        return False
