'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: mailSender
Description:
    Accepts receiver, subject and mailBody as input and sends an
    email to the receiver with the subject and mailBody
----------------------------------------------
'''

from smtplib import SMTP_SSL \
                    , SMTPException \
                    , SMTPAuthenticationError \
                    , SMTPConnectError \
                    , SMTPServerDisconnected \
                    , SMTPHeloError
import logging

from email.message import EmailMessage
from .config_reader import Configs

logger = logging.getLogger("main.mail_sender")

def send_email(receiver, subject, mail_body, default=False):
    '''
    Inputs: receiver(str), subject(str), mailBody(str), default(boolean)
    Description:
        Sends email to given receiver, with given subject and mailBody
        If default = true, sends email to default sender specified in credentials
    Return:
        status(int), error(Exception object)
    '''
    if default:
        receiver = Configs.EMAIL_ADDRESS

    message = EmailMessage()
    message['From'] = Configs.EMAIL_ADDRESS
    message['To'] = receiver
    message['Subject'] = subject

    message.set_content(mail_body)

    message.add_alternative(mail_body, subtype='html')

    #Create SMTP session for sending the mail
    status = 0
    error = None
    error_count = 0

    while error_count < Configs.MAX_RETRY_LIMIT:
        try:
            session = SMTP_SSL(Configs.MAIL_HOST, Configs.MAIL_PORT_NUMBER)
            session.login(Configs.EMAIL_ADDRESS, Configs.PASSWORD)
            session.send_message(message)
            session.quit()
            status = 1
            error = None
            break

        except SMTPConnectError as smtp_connect:
            status, error = 0, smtp_connect
            logger.warning("An error occurred during establishment of a connection with the server")
            error_count += 1

        except SMTPAuthenticationError as smtp_auth:
            status, error = 0, smtp_auth
            logger.error("The username/password given in the credentials file is invalid")
            break

        except SMTPServerDisconnected as smtp_disconnect:
            status, error = 0, smtp_disconnect
            logger.warning("The server disconnected unexpectedly")
            error_count += 1

        except SMTPHeloError as smtp_helo:
            status, error = 0, smtp_helo
            logger.warning("The server refused the HELO message")
            error_count += 1

        except SMTPException as smtp_exc:
            status, error = 0, smtp_exc
            logger.warning("An SMTP exception occurred: %s", smtp_exc)
            error_count += 1

        except TimeoutError as time_out:
            status, error = 0, time_out
            logger.warning("The connection operation timed out. Details: %s", time_out)
            error_count += 1

        except Exception as exc:
            status, error = 0, exc
            logger.exception("An unexpected fatal error occurred. Details: %s", exc)
            break

    return status, error
