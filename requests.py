"""
Project: Reappropriation

Author: Karandeep Singh Nagra

Convert the processed output from all_<rtype>.txt using requests.awk
into Django DB entries.
"""

from farnsworth.legacy.models import TeacherRequest, TeacherResponse

from .utils import read_dict, process_timestamp


def save_request(obj_dict, rtype, timestamp):
    """
    Create a TeacherRequest object from the given dictionary.
    obj_dict should be a dictionary with all values necessary
    for generating a new TeacherRequest.
    rtype is the request type and should be either 'food' or 'maintenance'.
    timestamp should be a processed datetime object.
    """
    request = TeacherRequest(obj_dict)
    request.request_type = rtype
    request.timestamp = timestamp
    request.save()

def save_response(obj_dict, rtype, timestamp):
    """
    Create a TeacherResponse object from the given dictionary.
    obj_dict should be of form {'teacher_key': tk, 'response': rdict},
    where rdict is a dictionary with all values necessary for
    generating a new TeacherResponse.
    rtype is the request type and should be either 'food' or 'maintenance'.
    timestamp should be a processed datetime object.
    """
    request = TeacherRequest.objects.get(
        teacher_key=obj_dict['teacher_key'],
        request_type = rtype
    )
    response = TeacherResponse(obj_dict['response'])
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

def process_requests(log_file_name, food_file_name, maint_file_name):
    """
    Process all request files.
    """
    process_requests_file(food_file_name, 'food', log_file_name)
    process_requests_file(maint_file_name, 'maintenance', log_file_name)
