"""
Functionality related to printing logs.
"""
import os
from datetime import datetime

def log_message(msg: str):
    """
    Print a message to output.
    :param msg:
    """
    pid = os.getpid()
    print(f'[pid:{pid}][date:{datetime.now()}][msg:{msg}]')