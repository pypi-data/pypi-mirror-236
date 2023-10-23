""" common predicates """

from os import path
from typing import Any
from typing import Optional


def is_not_none(x:Optional[Any])->bool:
    """ util """
    return x is not None

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
