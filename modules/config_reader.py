'''
----------------------------------------------
Project: CoWIN Slot Notifier
Module: config_reader
Description:
    Accepts file name and initializes
    configurations from the file
----------------------------------------------
'''

import os
import json
import logging

class Configs:
    """
    Description:
        Stores config values in class variables
    Methods:
        load_configs
    """

    @classmethod
    def load_configs(cls, config_filename):
        """
        Inputs: config_filename(str), subject(str), mailBody(str), default(boolean)
        Description:
            Sends email to given receiver, with given subject and mailBody
            If default = true, sends email to default sender specified in credentials
        Return:
            status(int), error(Exception object)
        """
        logger = logging.getLogger("main.config_reader")
        cur_path = os.path.dirname(__file__)
        new_filename = os.path.normpath(os.path.join(cur_path, '..', 'files', config_filename))
        error = None

        try:
            with open(new_filename, encoding='UTF-8') as f:
                configs = json.load(f)
        except FileNotFoundError as fnf:
            error = fnf
            logger.exception("FATAL ERROR: Configs file %s not found. Details: %s",
                            config_filename, fnf)
        except Exception as exc:
            error = exc
            logger.exception("FATAL ERROR: An unknown error occurred: %s", exc)

        if error:
            return 0, error

        main_configs = configs["main"]
        log_configs = configs["logging"]

        cls.PARAMS_FILENAME = main_configs["PARAMS_FILENAME"]
        cls.SLEEP_TIME = main_configs["SLEEP_TIME"]
        cls.ERROR_RECOVERY_TIME = main_configs["ERROR_RECOVERY_TIME"]
        cls.MAX_RETRY_LIMIT = main_configs["MAX_RETRY_LIMIT"]
        cls.MAIL_HOST = main_configs["MAIL_HOST"]
        cls.MAIL_PORT_NUMBER = main_configs["MAIL_PORT_NUMBER"]
        cls.CREDENTIALS_FILENAME = main_configs["CREDENTIALS_FILENAME"]
        cls.ERROR_SLEEP_TIME = main_configs["ERROR_SLEEP_TIME"]
        cls.STATES_REQUEST_URL = main_configs["STATES_REQUEST_URL"]
        cls.DISTRICTS_REQUEST_URL = main_configs["DISTRICTS_REQUEST_URL"]
        cls.REQUEST_BY_DIST_ID_URL = main_configs["REQUEST_BY_DIST_ID_URL"]
        cls.LOG_FILE_NAME = log_configs["LOG_FILE_NAME"]
        cls.FILE_LOG_LEVEL = log_configs["FILE_LOG_LEVEL"]

        new_filename = os.path.normpath(os.path.join(cur_path,
                                                    '..', 'files', cls.CREDENTIALS_FILENAME))

        try:
            with open(new_filename, encoding='UTF-8') as f:
                credentials = json.load(f)
        except FileNotFoundError as fnf:
            error = fnf
            logger.debug("FATAL ERROR: Credentials file %s not found. Details: %s",
                             cls.CREDENTIALS_FILENAME, fnf)
        except Exception as exc:
            error = exc
            logger.exception("FATAL ERROR: An unknown error occurred: %s", exc)

        if error:
            return 0, error

        cls.EMAIL_ADDRESS = credentials["username"]
        cls.PASSWORD = credentials["password"]

        return 1, None

    @classmethod
    def print_configs(cls):
        """
        Inputs: None
        Description:
            Prints configs (helper function)
        Return: None
        """
        print(cls.PARAMS_FILENAME)
        print(cls.SLEEP_TIME)
        print(cls.ERROR_RECOVERY_TIME)
        print(cls.MAX_RETRY_LIMIT)
        print(cls.MAIL_HOST)
        print(cls.MAIL_PORT_NUMBER)
        print(cls.CREDENTIALS_FILENAME)
        print(cls.ERROR_SLEEP_TIME)
        print(cls.STATES_REQUEST_URL)
        print(cls.DISTRICTS_REQUEST_URL)
        print(cls.REQUEST_BY_DIST_ID_URL)
        print(cls.LOG_FILE_NAME)
        print(cls.FILE_LOG_LEVEL)
