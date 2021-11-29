"""
Author: Gift Tangsupakij
Date: 11/24/2021
Description: Object models - defines properties of objects
"""

from django.db import models
from .utils import WorkStatus, ClockType, ViolationStatus


class Event(models.Model):
    """ Event represents driver working status """
    id = models.BigAutoField(primary_key=True)  # event id
    workStatus = models.CharField(max_length=3, choices=WorkStatus.options())  # work status (W, D, OFF)
    duration = models.DurationField(help_text="HH:MM:SS")  # time delta

    def __str__(self):
        return "{} - {}".format(self.workStatus, self.duration)


class Clock(models.Model):
    """ Clock represents how much time the driver has drove/worked"""
    type = models.CharField(max_length=11, choices=ClockType.options())  # clock type (drive clock, work clock)
    violationStatus = models.CharField(max_length=2, choices=ViolationStatus.options())  # violation status (V, OK)
    timeValue = models.DurationField(help_text="HH:MM:SS")  # time delta

    def __str__(self):
        return "{} - {}".format(self.type, self.violationStatus)
