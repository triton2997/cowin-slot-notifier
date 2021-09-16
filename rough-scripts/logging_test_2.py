import logging

LOG_LEVEL = "DEBUG"
FILE_NAME = "example.log"

NUMERIC_LEVEL = getattr(logging, LOG_LEVEL.upper(), None)
# logger.setLevel(NUMERIC_LEVEL)

# fh = logging.FileHandler("example.log")
# fh.setLevel(NUMERIC_LEVEL)

# formatter = logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
#                               datefmt='%m/%d/%Y %H:%M:%S')

# fh.setFormatter(formatter)

# logger.addHandler(fh)

# logging.basicConfig(format="%(asctime)s %(name)s %(levelname)s %(message)s",
#                     datefmt='%m/%d/%Y %H:%M:%S',
#                     filename='example.log',
#                     level=NUMERIC_LEVEL)
def do_something():
    if not isinstance(NUMERIC_LEVEL, int):
        raise ValueError('Invalid log level: {}'.format(LOG_LEVEL))

    logger = logging.getLogger("simple_example.level_2")
    logger.debug('This message should go to the log file')
    logger.info('So should this')
    logger.warning('And this, too')
    logger.error('And non-ASCII stuff, too, like Øresund and Malmö')

    try:
        raise ValueError("Test Error")
    except ValueError as e:
        logger.error(e)
        logger.exception(e)
