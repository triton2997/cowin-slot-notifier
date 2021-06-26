import requests
from datetime import date

# Config details are currently hardcoded
# Change this to use dictionary object supplied by getConfigProperties

sender = "cowinnotifiervignesh@gmail.com"

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
}

# Find Availability
def findAvailability(prop):

    request_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(prop["district_id"], date.today().strftime("%d-%m-%Y"))
    print(request_url)
    slots = []
    result = requests.get(request_url, headers=header)
    response_json = result.json()
    data = response_json["sessions"]
    count = 0
    for item in data:
        if (item["available_capacity"] > 0 
                and (prop["fee_type"] == "Any" or item["fee_type"] == prop["fee_type"]) 
                and item["min_age_limit"] >= prop["min_age"] 
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





