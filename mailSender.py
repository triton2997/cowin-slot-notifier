# app password directly put in plaintext
# change this to take it from props file instead
# Do not commit props file to git

import smtplib
import json
from email.message import EmailMessage


def sendEmail(receiver, subject, mailBody):

    #The mail addresses and password
    with open("credentials.json") as f:
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
    session = smtplib.SMTP_SSL('smtp.gmail.com', 465) #use gmail with port
    session.ehlo()
    session.login(SENDER_ADDRESS, SENDER_PASS) #login with mail_id and password
    
    session.send_message(message)
    session.quit()
    print('Mail Sent')