""" common predicates """

from typing import Any
from typing import Optional


def is_not_none(x:Optional[Any])->bool:
    """ util """
    return x is not None
