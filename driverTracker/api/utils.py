"""
Author: Gift Tangsupakij
Date: 11/24/2021
Description: Model parameter definition set
"""

from enum import Enum


class WorkStatus(Enum):
    """ Possible work status values """
    D = "driving"
    W = "working"
    OFF = "off_duty"

    @classmethod
    def options(cls):
        return [(opt.name, opt.value) for opt in cls]


class ClockType(Enum):
    """ Possible clock types """
    DRIVE_CLOCK = "drive clock"
    WORK_CLOCK = "work clock"

    @classmethod
    def options(cls):
        return [(opt.name, opt.value) for opt in cls]


class ViolationStatus(Enum):
    """ Possible violation statuses """
    V = "violation"
    OK = "not in violation"

    @classmethod
    def options(cls):
        return [(opt.name, opt.value) for opt in cls]
