from modules.cowinSlotsFinder import findAvailability

params = {'label': 'Vignesh 1st dose', 
        'state': 'Maharashtra', 
        'district': 'Mumbai', 
        'email_id': 'vignesh2997@gmail.com', 
        'fee_type': 'Paid', 
        'min_age': 18, 
        'vaccine': 'COVISHIELD', 
        'dose_number': 1, 
        'pincodes': {400092, 400067}}

slots, count = findAvailability(params)

print(slots, count)
