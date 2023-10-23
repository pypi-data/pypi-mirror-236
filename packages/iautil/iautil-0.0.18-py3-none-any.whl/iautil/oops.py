#cython: language_level=3

""" errors """

class UnexpectedExecutionPathError(AssertionError):
    """ did not expect to go there """
