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

def getConfigProperties(filename):
    prop_dicts = []

    cur_path = cur_path = os.path.dirname(__file__)
    new_filename = os.path.normpath(os.path.join(cur_path, '..', 'files', filename))

    with open(new_filename) as f:
        data = json.load(f)
    
    for item in data['configs']:
        prop_dict = {}
        if ("state" not in item 
            or "district" not in item
            or "email_id" not in item
            or "label" not in item
            or "id" not in item):
            print("Invalid configuration")
        else:
            prop_dict["id"] = item["id"]
            prop_dict["label"] = item["label"]
            prop_dict["state"] = item["state"]
            prop_dict["district"] = item["district"]
            prop_dict["email_id"] = item["email_id"]
            prop_dict["fee_type"] = item["fee_type"] if "fee_type" in item else "Any"
            prop_dict["min_age"] = int(item["min_age"]) if "min_age" in item else 18
            prop_dict["vaccine"] = item["vaccine"] if "vaccine" in item else "Any"
            prop_dict["dose_number"] = int(item["dose_number"]) if "dose_number" in item else 0
            prop_dict["pincodes"] = set([int(x) for x in item["pincodes"]]) if "pincodes" in item else []

            prop_dicts.append(prop_dict)

    return prop_dicts
