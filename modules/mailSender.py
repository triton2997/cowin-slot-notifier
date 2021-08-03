'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: mailSender
Description:
    Accepts receiver, subject and mailBody as input and sends an
    email to the receiver with the subject and mailBody
----------------------------------------------
'''

import os
from smtplib import SMTP_SSL \
                    , SMTPException \
                    , SMTPAuthenticationError \
                    , SMTPConnectError \
                    , SMTPServerDisconnected \
                    , SMTPHeloError
import json

from email.message import EmailMessage

CREDENTIALS_FILENAME = "credentials.json"
MAIL_PROVIDER = "smtp.gmail.com"
PORT_NUMBER = 465
MAX_ERROR_LIMIT = 5

def sendEmail(receiver, subject, mailBody, default=False):
    '''
    Inputs: receiver(str), subject(str), mailBody(str), default(boolean)
    Description:
        Sends email to given receiver, with given subject and mailBody
        If default = true, sends email to default sender specified in credentials
    Return:
        status(int), error(Exception object)
    '''
    #Load mail addresses and password
    cur_path = cur_path = os.path.dirname(__file__)
    new_filename = os.path.normpath(os.path.join(cur_path, '..', 'files', CREDENTIALS_FILENAME))
    error = None

    try:
        with open(new_filename) as f:
            credentials = json.load(f)
    except FileNotFoundError as fnf:
        error = fnf
    except Exception as exc:
        error = exc

    if error:
        return 0, error

    SENDER_ADDRESS = credentials["username"]
    SENDER_PASS = credentials["password"]

    if default:
        receiver = SENDER_ADDRESS

    message = EmailMessage()
    message['From'] = SENDER_ADDRESS
    message['To'] = receiver
    message['Subject'] = subject

    message.set_content(mailBody)

    message.add_alternative(mailBody, subtype='html')

    #Create SMTP session for sending the mail
    status = 0
    error = None
    error_count = 0

    while error_count < MAX_ERROR_LIMIT:
        try:
            session = SMTP_SSL(MAIL_PROVIDER, PORT_NUMBER)
            session.ehlo()
            session.login(SENDER_ADDRESS, SENDER_PASS)
            session.send_message(message)
            session.quit()
            status = 1
            error = None
            break

        except SMTPConnectError as smtp_connect:
            status, error = 0, smtp_connect
            print("An error occurred during establishment of a connection with the server")
            error_count += 1

        except SMTPAuthenticationError as smtp_auth:
            status, error = 0, smtp_auth
            print("The username/password given is invalid")
            break

        except SMTPServerDisconnected as smtp_disconnect:
            status, error = 0, smtp_disconnect
            print("The server disconnected unexpectedly")
            error_count += 1

        except SMTPHeloError as smtp_helo:
            status, error = 0, smtp_helo
            print("The server refused the HELO message")
            error_count += 1

        except SMTPException as smtp_exc:
            status, error = 0, smtp_exc
            print("An SMTP exception occurred", smtp_exc)
            error_count += 1

        except TimeoutError as time_out:
            status, error = 0, time_out
            print("The connection operation timed out. Details:", time_out)
            error_count += 1

        except Exception as exc:
            status, error = 0, exc
            print("An unexpected fatal error occurred", exc)
            error_count += 1

    return status, error
