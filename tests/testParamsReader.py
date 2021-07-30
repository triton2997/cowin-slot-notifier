from modules.paramsReader import getParams

CONFIG_FILENAME = 'test_params.json'

test_output = \
[
    {'id': '1', 'label': 'Test 1', 'state': 'State', 
     'district': 'District', 'email_id': 'email@example.com', 
     'fee_type': 'Free', 'min_age': 18, 'vaccine': 'COVISHIELD', 
     'dose_number': 2, 'pincodes': {1234, 5678}
    }, 
    {'id': '2', 'label': 'Test 2', 'state': 'State', 
     'district': 'District', 'email_id': 'email@example.com', 
     'fee_type': 'Free', 'min_age': 18, 'vaccine': 'Any', 
     'dose_number': 0, 'pincodes': []
    }, 
    {'id': '3', 'label': 'Test 3', 'state': 'State', 
     'district': 'District', 'email_id': 'email@example.com', 
     'fee_type': 'Any', 'min_age': 18, 'vaccine': 'Any', 
     'dose_number': 0, 'pincodes': []
    },
    {'id': '4', 'label': 'Test 4', 'state': 'State', 
     'district': 'District', 'email_id': 'email@example.com', 
     'fee_type': 'Any', 'min_age': 18, 'vaccine': 'COVISHIELD', 
     'dose_number': 0, 'pincodes': []
    },
    {'id': '5', 'label': 'Test 5', 'state': 'State', 
     'district': 'District', 'email_id': 'email@example.com', 
     'fee_type': 'Any', 'min_age': 18, 'vaccine': 'Any', 
     'dose_number': 2, 'pincodes': []
    },
    {'id': '6', 'label': 'Test 6', 'state': 'State', 
     'district': 'District', 'email_id': 'email@example.com', 
     'fee_type': 'Any', 'min_age': 18, 'vaccine': 'Any', 
     'dose_number': 0, 'pincodes': {1234, 5678}
    }
]

props, error = getParams(CONFIG_FILENAME)

if error:
    print("Error occurred:", error)

else:
    fail = {}
    flag = True

    for idx, dict_op in enumerate(test_output):
        prop_dict = props[idx]
        fail_dict = {}
        for key in dict_op:
            if prop_dict[key] != dict_op[key]:
                fail_dict[key] = [dict_op[key], prop_dict[key]]

        if len(fail_dict) > 0:
            flag = False
            fail[dict_op["label"]] = fail_dict

    if not flag:
        print("Test failed")
        print(fail)

    else:
        print("Test passed")

