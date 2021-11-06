'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: configPropertiesReader
Description:
    Reads config parameters from json file and returns a list of dictionaries,
    each dictionary specifying a set of parameters
----------------------------------------------
'''

import os
import json

import logging

logger = logging.getLogger("main.params_reader")

def get_params(filename):
    '''
    Inputs: filename(str)
    Description:
        Reads params json file given by filename and creates a list of dictionary objects
        For each set of parameters in json file, a dictionary is created
        and basic type checking is performed
    Return:
        param_dicts(List[dict]), error(Exception object)
    '''
    param_dicts = []

    cur_path = cur_path = os.path.dirname(__file__)
    new_filename = os.path.normpath(os.path.join(cur_path, '..', 'files', filename))
    error = None
    try:
        with open(new_filename, encoding='UTF-8') as f:
            data = json.load(f)
    except FileNotFoundError as fnf:
        error = fnf
        logger.exception("FATAL ERROR: Params file %s not found. Details: %s", filename, fnf)
    except Exception as exc:
        error = exc
        logger.exception("FATAL ERROR: An unknown error occurred: %s", exc)

    if error:
        return None, error

    for item in data['params']:
        param_dict = {}
        if ("state" not in item
            or "district" not in item
            or "email_id" not in item
            or "label" not in item
            or "id" not in item):
            print("Invalid configuration")
        else:
            param_dict["id"] = item["id"]
            param_dict["label"] = item["label"]
            param_dict["state"] = item["state"]
            param_dict["district"] = item["district"]
            param_dict["email_id"] = item["email_id"]
            param_dict["fee_type"] = item["fee_type"] if "fee_type" in item else "Any"
            param_dict["min_age"] = int(item["min_age"]) if "min_age" in item else 18
            param_dict["vaccine"] = item["vaccine"] if "vaccine" in item else "Any"
            param_dict["dose_number"] = int(item["dose_number"]) if "dose_number" in item else 0
            param_dict["pincodes"] = set([int(x) for x in item["pincodes"]]) \
                                     if "pincodes" in item else []

            param_dicts.append(param_dict)

    return param_dicts, None
