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
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException

from modules.cowinSlotsFinder import findAvailability
from modules.mailBodyGenerator import generateMailBody
from modules.mailSender import sendEmail
from modules.configPropertiesReader import getConfigProperties

CONFIG_FILENAME = 'config.json'

# Interval to ensure number of API calls does not exceed 100 in 5 minutess
SLEEP_TIME = 15
ERROR_COUNTER = 0
MAX_ERROR_COUNT = 5

while True:
    print("Check at {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    props = getConfigProperties(CONFIG_FILENAME)

    for prop in props:
        slots, response_code, error = findAvailability(prop)
        count = len(slots) if slots else 0

        if error:
            if error == Timeout:
                print("Request timed out")
            elif error == ConnectionError:
                print("An error occurred while establishing the connection")
            elif error == HTTPError:
                print("An HTTPError occurred:",error)
            elif error == RequestException:
                print("A fatal error occurred")
        
            ERROR_COUNTER += 1
            if ERROR_COUNTER > MAX_ERROR_COUNT:
                status, error = sendEmail("", "Fatal error occurred", "A fatal error occurred: {}".format(error), default=True)
                break
        
        elif response_code == -1:
            subject = "Invalid state/district configured for label - {}".format(prop["label"])
            mailBody = """Invalid state/district configured. Please update the state/district
            State: {}
            District: {}
            """.format(prop["state"], prop["district"])

        else:
            ERROR_COUNTER = 0
            if count > 0:
                mailBody = generateMailBody(slots, prop["dose_number"])
                subject = "Slots available for label - {}!".format(prop["label"])
                status, error = sendEmail(prop["email_id"], subject, mailBody)
                if error:
                    print("Fatal error occurred while sending email for label", prop["label"], error)

            
        print("{} slots found".format(count))

        sleep(SLEEP_TIME)
