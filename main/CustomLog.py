import os
import logging

def setup_custom_logger(name, log_level = logging.DEBUG):
    
    if log_level == 'INFO':
        log_level = logging.INFO
    elif log_level == 'WARNING':
        log_level = logging.WARNING
    else:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)

    logger = logging.getLogger(name)

    # create a file handler
    log_dirs = os.path.join(os.path.dirname( __file__ ), '..', 'logs')
    if not os.path.isdir(log_dirs):
        os.mkdir(log_dirs)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Log in the file
    fh = logging.FileHandler(os.path.join(os.path.dirname( __file__ ), '..', 'logs', 'main.log'))
    fh.setLevel(log_level)
    fh.setFormatter(formatter)

    # Log in the file
    sh = logging.StreamHandler()
    sh.setLevel(log_level)
    sh.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(sh)

    return logger
