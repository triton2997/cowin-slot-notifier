'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: cowinSlotsFinder
Description:
    Accepts dictionary object with parameters as input and returns available 
    slots based on the parameters
----------------------------------------------
'''

import requests
from datetime import date as dt
from datetime import timedelta

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

def safeRequest(request_url):
    response = None
    response_code = 0
    error = None

    try:
        response = requests.get(request_url, headers = header)
        response_code = response.status_code
        response.raise_for_status()
    except requests.exceptions.Timeout as to:
        print("Request timed out")
        error = to
    except requests.exceptions.ConnectionError as ce:
        print("Connection error")
        error = ce
    except requests.exceptions.HTTPError as http:
        print("Http error:", http)
        error = http
    except requests.exceptions.RequestException as e:
        print("Fatal error:", e)
        error = e
    
    return response, response_code, error

# Get district ID
def getDistrictID(state_name, district_name):
    """Returns district_ID using given state_name and district_name"""

    # get list of states
    states_request_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"

    result, response_code, error = safeRequest(states_request_URL)
    
    if response_code != requests.codes.ok:
        return 0, response_code, error

    response_json = result.json()

    # filter for given state and get state ID
    state_id = 0
    for state in response_json["states"]:
        if state["state_name"] == state_name:
            state_id = state["state_id"]
            break

    if state_id == 0:
        return -1, response_code, error

    # get list of districts by state ID
    districts_request_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_id)

    result, response_code, error = safeRequest(districts_request_URL)
    
    if response_code != requests.codes.ok:
        return 0, response_code, error
    
    response_json = result.json()

    # filter for given district
    for district in response_json["districts"]:
        if district["district_name"] == district_name:
            return district["district_id"], 200, None
    
    return -1, response_code, error

# Find Availability by date
def findAvailabilityByDate(prop, district_id, date):
    """Returns slots filtered by parameters for the given district on a given date"""

    request_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(district_id, date)
    slots = []
    
    result, response_code, error = safeRequest(request_url)
    
    if response_code != requests.codes.ok:
        return 0, response_code, error
    
    response_json = result.json()
    data = response_json["sessions"]
    count = 0
    for item in data:
        if (item["available_capacity"] > 0 
                and (prop["fee_type"] == "Any" or item["fee_type"] == prop["fee_type"]) 
                and item["min_age_limit"] == prop["min_age"] 
                and (prop["vaccine"] == "Any" or item["vaccine"] == prop["vaccine"]) 
                and (len(prop["pincodes"]) == 0 or item["pincode"] in prop["pincodes"]) 
                and (prop["dose_number"] == 0 or item["available_capacity_dose{}".format(prop["dose_number"])] > 0)):
            count += 1
            slot = [count, item["name"], item["address"], item["pincode"], item["available_capacity"]]
            if prop["dose_number"] in {0,1}:
                slot.append(item["available_capacity_dose1"])
            
            if prop["dose_number"] in {0,2}:
                slot.append(item["available_capacity_dose2"])
            slot.append(item["date"])
            slot.append("{} - {}".format(item["from"], item["to"]))
            slots.append(slot)
    
    return slots, response_code, None

# Find Availability
def findAvailability(prop):
    """Returns slots for current date and next date"""

    district_id, response_code, error = getDistrictID(prop["state"], prop["district"])
    if district_id == -1 or error:
        return None, -1, error
    
    today = dt.today()
    dates = [today.strftime("%d-%m-%Y"), today + timedelta(days=1)]
    slots = []

    for date in dates:
        slots_by_date, response_code, error = findAvailabilityByDate(prop, district_id, date)
        if not error:
            slots += slots_by_date

    return slots, response_code, error