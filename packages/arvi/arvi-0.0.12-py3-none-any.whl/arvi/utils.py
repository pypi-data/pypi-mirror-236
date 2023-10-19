import os
from contextlib import contextmanager
try:
    from unittest.mock import patch
except ImportError:
    try:
        from mock import patch
    except ImportError as e:
        raise e

import logging


def create_directory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

@contextmanager
def stdout_disabled():
    devnull = open(os.devnull, 'w')
    with patch('sys.stdout', devnull):
        yield


@contextmanager
def all_logging_disabled():
    """
    A context manager that will prevent any logging messages triggered during
    the body from being processed.
    """
    # two kind-of hacks here:
    #    * can't get the highest logging level in effect => delegate to the user
    #    * can't get the current module-level override => use an undocumented
    #       (but non-private!) interface

    previous_level = logging.root.manager.disable

    logging.disable(logging.CRITICAL)

    try:
        yield
    finally:
        logging.disable(previous_level)
