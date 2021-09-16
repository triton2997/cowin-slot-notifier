import logging
import logging.handlers

LOG_LEVEL = "DEBUG"
FILE_NAME = "example.log"

NUMERIC_LEVEL = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(NUMERIC_LEVEL, int):
    raise ValueError('Invalid log level: {}'.format(LOG_LEVEL))



logger = logging.getLogger("simple_example")
logger.setLevel(NUMERIC_LEVEL)

fh = logging.FileHandler("logs/example.log")
fh.setLevel(NUMERIC_LEVEL)

fh2 = logging.handlers.SMTPHandler(mailhost="smtp.gmail.com",
                          fromaddr="vignesh2997@gmail.com",
                          toaddrs="vignesh2997@gmail.com",
                          subject="ERROR: Test logging email",
                          credentials=("vignesh2997@gmail.com", "jtjtbogwygsnarkz"),
                          secure=())
fh2.setLevel(logging.ERROR)

formatter = logging.Formatter(fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
                              datefmt='%m/%d/%Y %H:%M:%S')

fh.setFormatter(formatter)
fh2.setFormatter(formatter)

logger.addHandler(fh)
# logger.addHandler(fh2)

logger.debug('This message should go to the log file')
logger.info('So should this')
logger.warning('And this, too')
logger.error('This one will send an email and go to the file, with non-ASCII stuff, too, like Øresund and Malmö')

try:
    raise ValueError("Test Error")
except ValueError as e:
    logger.error(e)
    logger.exception("A fatal error occurred: {}".format(e))

