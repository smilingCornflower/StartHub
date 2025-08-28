import json
from unittest.mock import MagicMock

from django.utils.datastructures import MultiValueDict


def python_obj_to_mock_request(data_dict, files_dict=None):
    request = MagicMock()

    request.data = {}
    for key, value in data_dict.items():
        if isinstance(value, (dict, list)):
            request.data[key] = json.dumps(value)
        else:
            request.data[key] = value

    if files_dict:
        multivalue_files = {}
        for key, value in files_dict.items():
            if isinstance(value, list):
                multivalue_files[key] = value
            else:
                multivalue_files[key] = [value]
        request.FILES = MultiValueDict(multivalue_files)
    else:
        request.FILES = MultiValueDict()

    return request
