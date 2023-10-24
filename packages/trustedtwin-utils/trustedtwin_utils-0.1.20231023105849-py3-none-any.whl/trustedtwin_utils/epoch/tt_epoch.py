"""Stores definition of solutions related to usage of unix epoch"""
from time import time


def utc_now_epoch() -> float:
    """Return utc now time in unix epoch (with three digits precision e.g. 1680172454.123)"""

    return round(time(), 3)
