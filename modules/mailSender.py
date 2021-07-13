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
import smtplib
import json

from email.message import EmailMessage

CREDENTIALS_FILENAME = "credentials.json"
MAIL_PROVIDER = "smtp.gmail.com"
PORT_NUMBER = 465

def sendEmail(receiver, subject, mailBody):

    #Load mail addresses and password
    cur_path = cur_path = os.path.dirname(__file__)
    new_filename = os.path.join(cur_path, '..', 'files', CREDENTIALS_FILENAME)

    with open(new_filename) as f:
        credentials = json.load(f)
    
    SENDER_ADDRESS = credentials["username"]
    SENDER_PASS = credentials["password"]
    
    message = EmailMessage()
    message['From'] = SENDER_ADDRESS
    message['To'] = receiver
    message['Subject'] = subject
    
    message.set_content(mailBody)

    message.add_alternative(mailBody, subtype = 'html')

    #Create SMTP session for sending the mail
    session = smtplib.SMTP_SSL(MAIL_PROVIDER, PORT_NUMBER)
    session.ehlo()
    session.login(SENDER_ADDRESS, SENDER_PASS)
    
    session.send_message(message)
    session.quit()
    print('Mail Sent')