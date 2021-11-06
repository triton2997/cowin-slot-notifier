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
import logging
import logging.handlers

from requests import exceptions, codes



from modules.cowin_slots_finder import find_availability
from modules.mail_body_generator import generate_mail_body
from modules.mail_sender import send_email
from modules.params_reader import get_params
from modules.config_reader import Configs

CONFIG_FILENAME = "configs.json"

status, error = Configs.load_configs(CONFIG_FILENAME)
if not status:
    print(error)
    sys.exit()

# Configs.print_configs()

# configure logging
NUMERIC_LEVEL = getattr(logging, Configs.FILE_LOG_LEVEL.upper(), None)
if not isinstance(NUMERIC_LEVEL, int):
    raise ValueError(f'Invalid log level: {Configs.FILE_LOG_LEVEL}')

SUBJECT = "ERROR: An error occurred"
logger = logging.getLogger("main")
logger.setLevel(NUMERIC_LEVEL)

file_handler = logging.FileHandler(f"logs/{Configs.LOG_FILE_NAME}")
file_handler.setLevel(NUMERIC_LEVEL)

smtp_handler = logging.handlers.SMTPHandler(mailhost=Configs.MAIL_HOST,
                          fromaddr=Configs.EMAIL_ADDRESS,
                          toaddrs=Configs.EMAIL_ADDRESS,
                          subject=SUBJECT,
                          credentials=(Configs.EMAIL_ADDRESS, Configs.PASSWORD),
                          secure=())
smtp_handler.setLevel(logging.ERROR)

formatter = logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
                              datefmt='%m/%d/%Y %H:%M:%S')

file_handler.setFormatter(formatter)
smtp_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(smtp_handler)

while True:
    print(f"Check at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    params, error = get_params(Configs.PARAMS_FILENAME)
    if error.__class__ == FileNotFoundError:
        # status, mail_error = sendEmail("", "FATAL ERROR: Params file not found",
        #                           "Params file named {} not found".format(CONFIG_FILENAME),
        #                           default=True)
        # print("No such file found:", CONFIG_FILENAME)
        # if mail_error:
        #     print("An error occurred while sending the error email:", mail_error)
        sys.exit()

    elif error.__class__ == Exception:
        # status, mail_error = sendEmail("", "FATAL ERROR: An unknown fatal error occurred",
        #                           "An unkown fatal error occurred\nDetails: {}".format(error),
        #                           default=True)
        # print("A fatal error occurred:", error)
        # logger.exception("A fatal error occurred: {}".format(error))
        # if mail_error:
        #     print("An error occurred while sending the error email:", mail_error)
        sys.exit()

    elif error:
        # status, mail_error = sendEmail("", "FATAL ERROR: An unknown fatal error occurred",
        #                           "An unkown fatal error occurred\nDetails: {}".format(error),
        #                           default=True)
        # print("A fatal error occurred:", error)
        # logger.exception("A fatal error occurred: {}".format(error))
        # if mail_error:
        #     print("An error occurred while sending the error email:", mail_error)
        sys.exit()

    for param in params:
        slots, response_code, error = find_availability(param)
        COUNT = len(slots) if slots else 0

        if error:
            if error.__class__ == exceptions.Timeout:
                logger.debug("Exiting as connection timed out repeatedly")
                sys.exit()
            elif error.__class__ == exceptions.ConnectionError:
                logger.debug("Exiting due to repeated connection errors")
                sys.exit()
            elif error.__class__ == exceptions.HTTPError and response_code == codes.unauthorized:
                    # print("Invalid URL configured.Stopping...")
                    # status, mail_error = sendEmail("", "ERROR: Invalid URL configured",
                    #                           "An unrecoverable error occurred: {}".format(error),
                    #                             default=True)
                    # if mail_error:
                    #     print("An error occurred while sending the error email:", mail_error)
                logger.debug("Exiting due to HTTP 401 error")
                sys.exit()
            elif error.__class__ == exceptions.RequestException:
                # print("A fatal error occurred. Stopping...")
                # status, mail_error = sendEmail("", "ERROR: A fatal occurred",
                #                       """A non-recoverable fatal error occurred: {}\n
                #                       Program has stopped""".format(error),
                #                       default=True)
                # if mail_error:
                #     print("An error occurred while sending the error email:", mail_error)
                logger.debug("Exiting due to fatal error")
                sys.exit()

            # status, mail_error = sendEmail("", "ERROR: An error occurred",
            #                           "A recoverable error occurred: {}".format(error),
            #                           default=True)
            # if mail_error:
            #     print("An error occurred while sending the error email:", mail_error)
            logging.debug("Beginning error recovery...")
            sleep(Configs.ERROR_RECOVERY_TIME)

        elif response_code == -1:
            logger.exception("""
            Invalid state/district configured. Please update the state/district
            State: %s
            District: %s
            """, param["state"], param["district"])

        elif COUNT > 0:
            mailBody = generate_mail_body(slots, param["dose_number"])
            SUBJECT = f"Slots available for label - {param['label']}!"
            status, mail_error = send_email(param["email_id"], SUBJECT, mailBody)
            if not mail_error:
                print("Mail sent")


        print(f"{COUNT} slots found")

        sleep(Configs.SLEEP_TIME)
