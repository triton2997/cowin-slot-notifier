'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: Main
Description:
    Main module
    Runs check for all parameters given after a set interval
    Gets following details from a params file (* is required)
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

import sys
from time import sleep
from datetime import datetime, time
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException

from modules.cowinSlotsFinder import findAvailability
from modules.mailBodyGenerator import generateMailBody
from modules.mailSender import sendEmail
from modules.configPropertiesReader import getParams

CONFIG_FILENAME = 'params.json'

# Interval to ensure number of API calls does not exceed 100 in 5 minutess
SLEEP_TIME = 15
ERROR_RECOVERY_TIME = 300
MAX_ERROR_COUNT = 5

while True:
    print("Check at {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    params, error = getParams(CONFIG_FILENAME)
    if error.__class__ == FileNotFoundError:
        status, error = sendEmail("", "FATAL ERROR: Params file not found", "Params file named {} not found".format(CONFIG_FILENAME), default=True)
        print("No such file found:", CONFIG_FILENAME)
        sys.exit()
    
    elif error.__class__ == Exception:
        status, error = sendEmail("", "FATAL ERROR: An unknown fatal error occurred", "An unkown fatal error occurred\nDetails: {}".format(error), default=True)
        print("A fatal error occurred:", error)
        sys.exit()
    
    elif error:
        status, error = sendEmail("", "FATAL ERROR: An unknown fatal error occurred", "An unkown fatal error occurred\nDetails: {}".format(error), default=True)
        print("A fatal error occurred:", error)
        sys.exit()

    for param in params:
        slots, response_code, error = findAvailability(param)
        count = len(slots) if slots else 0

        if error:
            if error.__class__ == Timeout:
                print("Request timed out")
            elif error.__class__ == ConnectionError:
                print("An error occurred while establishing the connection")
            elif error.__class__ == HTTPError:
                print("An HTTPError occurred:",error)
            elif error.__class__ == RequestException:
                print("A fatal error occurred")

            status, error = sendEmail("", "ERROR: An error occurred", "A recoverable error occurred: {}".format(error), default=True)
            print("Error recovery...")
            sleep(ERROR_RECOVERY_TIME)
        
        elif response_code == -1:
            subject = "Invalid state/district configured for label - {}".format(param["label"])
            mailBody = """Invalid state/district configured. Please update the state/district
            State: {}
            District: {}
            """.format(param["state"], param["district"])

        elif count > 0:
            mailBody = generateMailBody(slots, param["dose_number"])
            subject = "Slots available for label - {}!".format(param["label"])
            status, error = sendEmail(param["email_id"], subject, mailBody)
            if error:
                print("Fatal error occurred while sending email for label", param["label"], error)
            print("Mail sent")

            
        print("{} slots found".format(count))

        sleep(SLEEP_TIME)
