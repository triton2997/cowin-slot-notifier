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
from datetime import datetime
from requests import exceptions, codes

from modules.cowinSlotsFinder import findAvailability
from modules.mailBodyGenerator import generateMailBody
from modules.mailSender import sendEmail
from modules.paramsReader import getParams

CONFIG_FILENAME = 'params.json'

# Interval to ensure number of API calls does not exceed 100 in 5 minutess
SLEEP_TIME = 15
ERROR_RECOVERY_TIME = 300
MAX_ERROR_COUNT = 5

while True:
    print("Check at {}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

    params, error = getParams(CONFIG_FILENAME)
    if error.__class__ == FileNotFoundError:
        status, mail_error = sendEmail("", "FATAL ERROR: Params file not found",
                                  "Params file named {} not found".format(CONFIG_FILENAME),
                                  default=True)
        print("No such file found:", CONFIG_FILENAME)
        if mail_error:
            print("An error occurred while sending the error email:", mail_error)
        sys.exit()

    elif error.__class__ == Exception:
        status, mail_error = sendEmail("", "FATAL ERROR: An unknown fatal error occurred",
                                  "An unkown fatal error occurred\nDetails: {}".format(error),
                                  default=True)
        print("A fatal error occurred:", error)
        if mail_error:
            print("An error occurred while sending the error email:", mail_error)
        sys.exit()

    elif error:
        status, mail_error = sendEmail("", "FATAL ERROR: An unknown fatal error occurred",
                                  "An unkown fatal error occurred\nDetails: {}".format(error),
                                  default=True)
        print("A fatal error occurred:", error)
        if mail_error:
            print("An error occurred while sending the error email:", mail_error)
        sys.exit()

    for param in params:
        slots, response_code, error = findAvailability(param)
        COUNT = len(slots) if slots else 0

        if error:
            if error.__class__ == exceptions.Timeout:
                print("Request timed out")
            elif error.__class__ == exceptions.ConnectionError:
                print("An error occurred while establishing the connection")
            elif error.__class__ == exceptions.HTTPError:
                print("An HTTPError occurred:", error)
                if response_code == codes.unauthorized:
                    print("Invalid URL configured.Stopping...")
                    status, mail_error = sendEmail("", "ERROR: Invalid URL configured",
                                                "An unrecoverable error occurred: {}".format(error),
                                                default=True)
                    if mail_error:
                        print("An error occurred while sending the error email:", mail_error)
                    sys.exit()
            elif error.__class__ == exceptions.RequestException:
                print("A fatal error occurred. Stopping...")
                status, mail_error = sendEmail("", "ERROR: A fatal occurred",
                                      """A non-recoverable fatal error occurred: {}\n
                                      Program has stopped""".format(error),
                                      default=True)
                if mail_error:
                    print("An error occurred while sending the error email:", mail_error)
                sys.exit()

            status, mail_error = sendEmail("", "ERROR: An error occurred",
                                      "A recoverable error occurred: {}".format(error),
                                      default=True)
            if mail_error:
                print("An error occurred while sending the error email:", mail_error)
            print("Error recovery...")
            sleep(ERROR_RECOVERY_TIME)

        elif response_code == -1:
            subject = "Invalid state/district configured for label - {}".format(param["label"])
            mailBody = """Invalid state/district configured. Please update the state/district
            State: {}
            District: {}
            """.format(param["state"], param["district"])
            status, mail_error = sendEmail("", subject, mailBody, default=True)
            if mail_error:
                print("An error occurred while sending the error email:", mail_error)

        elif COUNT > 0:
            mailBody = generateMailBody(slots, param["dose_number"])
            subject = "Slots available for label - {}!".format(param["label"])
            status, mail_error = sendEmail(param["email_id"], subject, mailBody)
            if mail_error:
                print("Fatal error occurred while sending email for label", param["label"], mail_error)
            else:
                print("Mail sent")


        print("{} slots found".format(COUNT))

        sleep(SLEEP_TIME)
