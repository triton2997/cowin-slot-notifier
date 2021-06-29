import requests
from datetime import date

# Config details are currently hardcoded
# Change this to use dictionary object supplied by getConfigProperties

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

# Get district ID
def getDistrictID(state, district):
    # get list of states
    states_request_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    result = requests.get(states_request_URL, header = header)
    response_json = result.json()

    # filter for given state and get state ID
    state_id = 0
    for state in response_json["states"]:
        if state["state_name"] == state:
            state_id = state["state_id"]
            break
    
    if state_id == 0:
        return -1

    # get list of districts by state ID
    districts_request_URL = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_id)
    result = requests.get(districts_request_URL, header = header)
    response_json = result.json()

    # filter for given district
    for district in response_json["districts"]:
        if district["district_name"] == district:
            return district["district_id"]
    
    return -1

# Find Availability
def findAvailability(prop):

    district_id = getDistrictID(prop["state"], prop["district"])
    if district_id == -1:
        return None, -1
    
    request_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(district_id, date.today().strftime("%d-%m-%Y"))
    slots = []
    result = requests.get(request_url, headers=header)
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
            slot = [count, item["name"], item["address"], item["available_capacity"]]
            if prop["dose_number"] in {0,1}:
                slot.append(item["available_capacity_dose1"])
            
            if prop["dose_number"] in {0,2}:
                slot.append(item["available_capacity_dose2"])

            slot.append("{} - {}".format(item["from"], item["to"]))
            slots.append(slot)

    return slots, count