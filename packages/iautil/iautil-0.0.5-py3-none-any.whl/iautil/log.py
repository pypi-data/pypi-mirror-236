""" common logging configuration """

from functools import wraps
import logging
import sys
import traceback
from typing import Any, Callable, TypeVar

T = TypeVar('T')

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


def handle_exception(logger:logging.Logger)->Callable[..., Callable[..., T]]:
    """
    Decorator function to handle exceptions and log error messages.
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        """ decorator """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            """ wrapper """
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error('Error: %s\n%s', e, traceback.format_exc())
                raise
        return wrapper
    return decorator

def trace(logger:logging.Logger)->Callable[..., Callable[..., T]]:
    """
    Decorator function to add tracing/logging functionality to any function
    """
    def decorator(func: Callable[..., T]) -> Callable[...,T]:
        """ decorator """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            """ wrapper """
            logger.debug('Entering %s', func.__name__)
            try:
                result = func(*args, **kwargs)
                logger.debug('Exiting %s', func.__name__)
                return result
            except:# Exception as e:
                logger.exception('Error in %s', func.__name__)
                raise# e
        return wrapper
    return decorator
