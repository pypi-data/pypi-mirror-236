""" common logging configuration """

from functools import wraps
from logging import getLogger, Logger, StreamHandler, Formatter, DEBUG
from sys import stdout
from traceback import format_exc
from typing import Callable, ParamSpec, TypeVar

T = TypeVar('T')
P = ParamSpec('P')

def configure_logging(name:str)->Logger:
    """ for docker """
    # Create a logger instance
    logger:Logger = getLogger(name)

    # Configure the logger to log to the console
    handler:StreamHandler = StreamHandler(stdout)
    handler.setLevel(DEBUG)

    # Configure the log format
    formatter:Formatter = Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    # Set the logger level
    logger.setLevel(DEBUG)

    return logger


def handle_exception(logger:Logger)->Callable[[Callable[P, T]], Callable[P, T]]:
    """
    Decorator function to handle exceptions and log error messages.
    """
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        """ decorator """
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """ wrapper """
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error('Error: %s\n%s', e, format_exc())
                raise
        return wrapper
    return decorator

def trace(logger:Logger)->Callable[[Callable[P,T]], Callable[P, T]]:
    """
    Decorator function to add tracing/logging functionality to any function
    """
    def decorator(func: Callable[P, T]) -> Callable[P,T]:
        """ decorator """
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            """ wrapper """
            logger.debug('Entering %s', func.__name__)
            try:
                result:T = func(*args, **kwargs)
                logger.debug('Exiting %s', func.__name__)
                return result
            except:# Exception as e:
                logger.exception('Error in %s', func.__name__)
                raise# e
        return wrapper
    return decorator
