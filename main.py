'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: Main
Description:
    Main module
    Runs check for all parameters given after a set interval
    Gets following details from a props file (* is required)
        District ID*
        Date*
        Email ID*
        Fee type
        Min Age
        Pincode list
        vaccine
        dose number
    Gets slots available based on above filters
    If slots are available, sends success email
    Else, goes into wait
----------------------------------------------
'''

from time import sleep
from datetime import datetime, time, timezone, timedelta

from modules.cowinSlotsFinder import findAvailability
from modules.mailBodyGenerator import generateMailBody
from modules.mailSender import sendEmail
from modules.configPropertiesReader import getConfigProperties

CONFIG_FILENAME = 'config.json'

# Interval for checking
SLEEP_TIME = 300 # 5 minutes

# If slots for a particular label are found, add it to a done list
done = set()

# Reset the done list at a set time everyday
# Currently set to 2:30 AM UTC (8 AM IST)
RESET_TIME = datetime.combine(datetime.utcnow().date(), time(2,30,0), tzinfo=timezone.utc)

while True:
    # Reset done list
    if datetime.now(timezone.utc) > RESET_TIME:
        done = set()
        RESET_TIME += timedelta(days = 1)

    print("Check at {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    props = getConfigProperties(CONFIG_FILENAME)

    for prop in props:
        if prop["id"] in done:
            continue

        slots, count = findAvailability(prop)

        if count == -1:
            subject = "Invalid state/district configured for label - {}".format(prop["label"])
            mailBody = """Invalid state/district configured. Please update the state/district
            State: {}
            District: {}
            """.format(prop["state"], prop["district"])

        elif count > 0:
                mailBody = generateMailBody(slots, prop["dose_number"])
                subject = "Slots available for label - {}!".format(prop["label"])
                sendEmail(prop["email_id"], subject, mailBody)
                done.add(prop["id"])
            
        print("{} slots found".format(count))
    
    print("Going into wait")

    sleep(SLEEP_TIME)
