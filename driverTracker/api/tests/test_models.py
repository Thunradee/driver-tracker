"""
Author: Gift Tangsupakij
Date: 11/24/2021
Description: Testing models
"""

from django.test import TestCase
from ..models import Event
from datetime import timedelta


class EventTest(TestCase):
    """ Test event model """
    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=3, minutes=30))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=1, minutes=5))

    def test_create_events(self):
        # test creating events
        w = Event.objects.get(workStatus='W')
        d = Event.objects.get(workStatus='D')
        off = Event.objects.get(workStatus='OFF')
        self.assertEqual(w.__str__(), 'W - 2:45:00')
        self.assertEqual(d.__str__(), 'D - 3:30:00')
        self.assertEqual(off.__str__(), 'OFF - 1:05:00')
