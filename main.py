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
from datetime import datetime, time

from modules.cowinSlotsFinder import findAvailability
from modules.mailBodyGenerator import generateMailBody
from modules.mailSender import sendEmail
from modules.configPropertiesReader import getConfigProperties

CONFIG_FILENAME = 'config.json'

# Interval to ensure number of API calls does not exceed 100 in 5 minutess
SLEEP_TIME = 15

while True:
    print("Check at {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    props = getConfigProperties(CONFIG_FILENAME)

    for prop in props:
        slots, response_code, error = findAvailability(prop)
        count = len(slots)

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
            
        print("{} slots found".format(count))

        sleep(SLEEP_TIME)
