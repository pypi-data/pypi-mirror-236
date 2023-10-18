""" common logging configuration """

import logging
import sys

def configure_logging(name:str)->logging.Logger:
    """ for docker """
    # Create a logger instance
    logger = logging.getLogger(name)

    # Configure the logger to log to the console
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    # Configure the log format
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # Set the logger level
    logger.setLevel(logging.DEBUG)

    return logger
