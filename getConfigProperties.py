# Get config details from configurations file
# Create a dictionary object for each properties item
# create a list of dictionary object
# return list of dictionary objects

import json



def getConfigProperties(filename):
    # using JSON

    prop_dicts = []

    with open('config.json',) as f:
        data = json.load(f)
    
    for item in data['configs']:
        prop_dict = {}
        if ("district_id" not in item 
            or "email_id" not in item):
            print("Invalid configuration")
        else:
            prop_dict["district_id"] = int(item["district_id"])
            prop_dict["email_id"] = item["email_id"]
            prop_dict["vaccine_type"] = item["vaccine_type"] if "vaccine_type" in item else "Any"
            prop_dict["fee_type"] = item["fee_type"] if "fee_type" in item else "Any"
            prop_dict["min_age"] = int(item["min_age"]) if "min_age" in item else 18
            prop_dict["vaccine"] = item["vaccine"] if "vaccine" in item else "Any"
            prop_dict["dose_number"] = int(item["dose_number"]) if "dose_number" in item else 0
            prop_dict["pincodes"] = set([int(x) for x in item["pincodes"]]) if "pincodes" in item else []

            prop_dicts.append(prop_dict)

    return prop_dicts
