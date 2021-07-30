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
from smtplib import SMTP_SSL, SMTPException, SMTPAuthenticationError, SMTPConnectError, SMTPServerDisconnected, SMTPHeloError
import json

from email.message import EmailMessage

CREDENTIALS_FILENAME = "credentials.json"
MAIL_PROVIDER = "smtp.gmail.com"
PORT_NUMBER = 465
MAX_ERROR_LIMIT = 5

def sendEmail(receiver, subject, mailBody, default=False):

    #Load mail addresses and password
    cur_path = cur_path = os.path.dirname(__file__)
    new_filename = os.path.normpath(os.path.join(cur_path, '..', 'files', CREDENTIALS_FILENAME))
    error = None

    try:
        with open(new_filename) as f:
            credentials = json.load(f)
    except FileNotFoundError as FNF:
        error = FNF
    except Exception as e:
        error = e
    
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

    message.add_alternative(mailBody, subtype = 'html')

    #Create SMTP session for sending the mail
    status = 0
    error = None
    ERROR_COUNTER = 0

    while ERROR_COUNTER < MAX_ERROR_LIMIT:
        try:
            session = SMTP_SSL(MAIL_PROVIDER, PORT_NUMBER)
            session.ehlo()
            session.login(SENDER_ADDRESS, SENDER_PASS)
            
            session.send_message(message)
            session.quit()
            status = 1
            error = None
            break

        except SMTPConnectError as e1:
            status, error = 0, e1
            print("An error occurred during establishment of a connection with the server")
            ERROR_COUNTER += 1
        
        except SMTPAuthenticationError as e2:
            status, error = 0, e2
            print("The username/password given is invalid")
            ERROR_COUNTER += 1
        
        except SMTPServerDisconnected as e3:
            status, error = 0, e3
            print("The server disconnected unexpectedly")
            ERROR_COUNTER += 1
        
        except SMTPHeloError as e4:
            status, error = 0, e4
            print("The server refused the HELO message")
            ERROR_COUNTER += 1
        
        except SMTPException as e:
            status, error = 0, e
            print("An unexpected fatal error occurred", e)
            ERROR_COUNTER += 1

    return status, error
    
