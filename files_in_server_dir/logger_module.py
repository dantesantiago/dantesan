import logging


def get_logger(log):
    logger = logging.getLogger(log.split('.')[0].split('/')[-1])

    logger.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s [%(process)d] %(levelname)s %(module)s.%(funcName)s: %(message)s')
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)

    return logger

