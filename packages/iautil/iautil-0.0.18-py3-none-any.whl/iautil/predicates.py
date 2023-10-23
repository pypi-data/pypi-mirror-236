#cython: language_level=3

""" common predicates """

from os import path
from typing import Any
from typing import Optional
#from pyfunctional import pure
from peval import pure


@pure
def is_none(x:Optional[Any])->bool:
    """ util """
    return x is None

@pure
def is_not_none(x:Optional[Any])->bool:
    """ util """
    return x is not None


@pure
def is_empty_string(s:str)->bool:
    return s == ''

@pure
def is_nonempty_string(s:str)->bool:
    return s != ''


def file_exists(file_path:str)->bool:
    """ path exists and is a regular file """
    if not path.exists(file_path):
        return False
    return path.isfile(file_path)

def dir_exists(file_path:str)->bool:
    """ path exists and is a directory """
    if not path.exists(file_path):
        return False
    return path.isdir(file_path)

def check_sock_exists(file_path:str)->bool:
    """ path exists and is a socket """
    raise NotImplementedError()
