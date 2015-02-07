import os
import logging

def setup_custom_logger(name, log_level = logging.DEBUG):
    logging.basicConfig(level=log_level)

    logger = logging.getLogger(name)

    # create a file handler
    handler = logging.FileHandler(os.path.join(os.path.dirname( __file__ ), '..', 'logs', 'main.log'))
    handler.setLevel(logging.DEBUG)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)

    return logger
