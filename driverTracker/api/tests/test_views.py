"""
Author: Gift Tangsupakij
Date: 11/24/2021
Description: Testing the view functions
"""

import json
from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import Event, Clock
from ..serializers import EventSerializer, ClockSerializer

# initialize the APIClient app
client = Client()


########################################################################
#                              Events                                  #
########################################################################


class GetAllEvents(TestCase):
    """ Test module for GET all events API """

    def setUp(self) -> None:
        # Set up environment for testing
        Event.objects.create(workStatus='D', duration=timedelta(hours=3, minutes=30))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=47))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=1, minutes=1))

    def test_get_all_events(self):
        # get API response
        response = client.get(reverse('get_post_events'))
        # get data from database
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        # confirm response to be as expected
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleEvent(TestCase):
    """ Test module for GET single event API """

    def setUp(self) -> None:
        # Set up environment for testing
        self.a1 = Event.objects.create(workStatus='D', duration=timedelta(hours=3, minutes=30))
        self.a2 = Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=47))
        self.a3 = Event.objects.create(workStatus='OFF', duration=timedelta(hours=1, minutes=1))

    def test_get_valid_single_event(self):
        # test valid case
        response = client.get(reverse('get_update_delete_event', kwargs={'pk': self.a2.pk}))
        event = Event.objects.get(pk=self.a2.pk)
        serializer = EventSerializer(event)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_event(self):
        # test invalid case
        response = client.get(reverse('get_update_delete_event', kwargs={'pk': 9}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostNewEventTest(TestCase):
    """ Test module for POST a new event """

    def setUp(self) -> None:
        # set up environment
        self.valid_data = {
            'workStatus': 'D',
            'duration': '3:30:00'
        }
        self.missing_work_status = {
            'duration': '3:30:00'
        }
        self.invalid_work_status = {
            'workStatus': 'driving',
            'duration': '3:30:00'
        }
        self.missing_duration = {
            'workStatus': 'D'
        }
        self.invalid_duration = {
            'workStatus': 'D',
            'duration': '3:30:00:00'
        }

    def test_post_valid_event(self):
        # test valid case
        response = client.post(reverse('get_post_events'),
                               data=json.dumps(self.valid_data),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_missing_work_status(self):
        # test POST request without work status
        response = client.post(reverse('get_post_events'),
                               data=json.dumps(self.missing_work_status),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_work_status(self):
        # test POST request with invalid work status
        response = client.post(reverse('get_post_events'),
                               data=json.dumps(self.invalid_work_status),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_missing_duration(self):
        # test POST request without time duration
        response = client.post(reverse('get_post_events'),
                               data=json.dumps(self.missing_duration),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_invalid_duration(self):
        # test POST request with invalid time duration
        response = client.post(reverse('get_post_events'),
                               data=json.dumps(self.invalid_duration),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleEvent(TestCase):
    """ Test module for PUT an existing event record """

    def setUp(self) -> None:
        # set up environment
        self.a1 = Event.objects.create(workStatus='D', duration=timedelta(hours=3, minutes=30))
        self.a2 = Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=47))
        self.a3 = Event.objects.create(workStatus='OFF', duration=timedelta(hours=1, minutes=1))

        self.valid_data = {
            'workStatus': 'W',
            'duration': '2:34:00'
        }
        self.missing_work_status = {
            'duration': '2:34:00'
        }
        self.invalid_work_status = {
            'workStatus': 'working',
            'duration': '2:34:00'
        }
        self.missing_duration = {
            'workStatus': 'W'
        }
        self.invalid_duration = {
            'workStatus': 'W',
            'duration': '2:34:00:00'
        }

    def test_valid_update_event(self):
        # test valid PUT request
        response = client.put(reverse('get_update_delete_event', kwargs={'pk': self.a1.pk}),
                              data=json.dumps(self.valid_data),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_missing_work_status(self):
        # test PUT request without work status
        response = client.put(reverse('get_update_delete_event', kwargs={'pk': self.a1.pk}),
                              data=json.dumps(self.missing_work_status),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_work_status(self):
        # test PUT request with invalid work status
        response = client.put(reverse('get_update_delete_event', kwargs={'pk': self.a1.pk}),
                              data=json.dumps(self.invalid_work_status),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_missing_duration(self):
        # test PUT request without time duration
        response = client.put(reverse('get_update_delete_event', kwargs={'pk': self.a1.pk}),
                              data=json.dumps(self.missing_duration),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_duration(self):
        # test PUT request with invalid time duration
        response = client.put(reverse('get_update_delete_event', kwargs={'pk': self.a1.pk}),
                              data=json.dumps(self.invalid_duration),
                              content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleEvent(TestCase):
    """ Test Module for DELETE an existing event record """

    def setUp(self) -> None:
        # set up environment
        self.a1 = Event.objects.create(workStatus='D', duration=timedelta(hours=3, minutes=30))
        self.a2 = Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=47))
        self.a3 = Event.objects.create(workStatus='OFF', duration=timedelta(hours=1, minutes=1))

    def test_valid_delete_single_event(self):
        # test valid DELETE request
        response = client.delete(reverse('get_update_delete_event', kwargs={'pk': self.a2.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_single_event(self):
        # test invalid DELETE request (with non-existent id)
        response = client.delete(reverse('get_update_delete_event', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

########################################################################
#                               Clocks                                 #
########################################################################


class GetClocks1(TestCase):
    """
    Test module for GET clocks API
    Example 1:
    D - 2 hours
    W - 1 hour
    OFF - 30 mins
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=2))
        Event.objects.create(workStatus='W', duration=timedelta(hours=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=30))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta(hours=2)),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta(hours=3, minutes=30))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks2(TestCase):
    """
    Test module for GET clocks API
    Example 2:
    D - 2 hours
    W - 1 hour
    OFF - 11 hours
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=2))
        Event.objects.create(workStatus='W', duration=timedelta(hours=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=11))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta()),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta())
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks3(TestCase):
    """
    Test module for GET clocks API
    Example 3:
    D - 2 hours
    W - 10 hours
    D - 3 hours
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=2))
        Event.objects.create(workStatus='W', duration=timedelta(hours=10))
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta(hours=5)),
            Clock(type='WORK_CLOCK', violationStatus='V', timeValue=timedelta(hours=15))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks4(TestCase):
    """
    Test module for GET clocks API
    Example 4:
    D - 2 hours
    OFF - 9 hours
    D - 2 hours
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=2))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=9))
        Event.objects.create(workStatus='D', duration=timedelta(hours=2))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta(hours=4)),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta(hours=13))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks5(TestCase):
    """
    Test module for GET clocks API
    Case: No event
    """

    def setUp(self) -> None:
        pass

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta()),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta())
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks6(TestCase):
    """
    Test module for GET clocks API
    Case:
    OFF - 11 hours
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=11))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta()),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta())
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks7(TestCase):
    """
    Test module for GET clocks API
    Case:
    OFF - 2 hours
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=2))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta()),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta(hours=2))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks8(TestCase):
    """
    Test module for GET clocks API
    Case:
    D - 3 hrs
    W - 1 hr 15 min
    OFF - 45 min
    D - 8 hrs
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=15))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=8))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta(hours=11)),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta(hours=14))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks9(TestCase):
    """
    Test module for GET clocks API
    Case:
    D - 3 hrs
    W - 1 hr 15 min
    OFF - 45 min
    D - 8 hrs 1 min
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=15))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=8, minutes=1))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='V', timeValue=timedelta(hours=11, minutes=1)),
            Clock(type='WORK_CLOCK', violationStatus='V', timeValue=timedelta(hours=14, minutes=1))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks10(TestCase):
    """
    Test module for GET clocks API
    Case:
    D - 3 hrs
    W - 1 hr 15 min
    OFF - 45 min
    D - 8 hrs 1 min
    OFF - 10 hr
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=15))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=8, minutes=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=10))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='V', timeValue=timedelta(hours=11, minutes=1)),
            Clock(type='WORK_CLOCK', violationStatus='V', timeValue=timedelta(hours=24, minutes=1))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks11(TestCase):
    """
    Test module for GET clocks API
    Case:
    D - 3 hrs
    W - 1 hr 15 min
    OFF - 45 min
    D - 8 hrs 1 min
    OFF - 10 hr
    OFF - 1 min
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=15))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=8, minutes=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=10))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=1))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta()),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta())
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks12(TestCase):
    """
    Test module for GET clocks API
    Case:
    D - 3 hrs
    W - 1 hr 15 min
    OFF - 45 min
    D - 8 hrs 1 min
    OFF - 11 hr
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=15))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=8, minutes=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=11))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta()),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta())
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks13(TestCase):
    """
    Test module for GET clocks API
    Case:
    D - 3 hrs
    W - 1 hr 15 min
    OFF - 45 min
    D - 8 hrs 1 min
    OFF - 11 hr
    W - 2 hrs
    D - 3 hrs
    W - 1 hr
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=15))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=8, minutes=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=11))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2))
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=1))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta(hours=3)),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta(hours=6))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks14(TestCase):
    """
    Test module for GET clocks API
    Case:
    D - 3 hrs
    W - 1 hr 15 min
    OFF - 45 min
    D - 8 hrs 1 min
    OFF - 11 hr
    W - 2 hrs
    D - 3 hrs
    W - 1 hr
    OFF - 1 hr
    D - 5 hrs
    W - 3 hrs 30 min
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=15))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=8, minutes=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=11))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2))
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=1))
        Event.objects.create(workStatus='D', duration=timedelta(hours=5))
        Event.objects.create(workStatus='W', duration=timedelta(hours=3, minutes=30))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta(hours=8)),
            Clock(type='WORK_CLOCK', violationStatus='V', timeValue=timedelta(hours=15, minutes=30))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetClocks15(TestCase):
    """
    Test module for GET clocks API
    Case:
    D - 3 hrs
    W - 1 hr 15 min
    OFF - 45 min
    D - 8 hrs 1 min
    OFF - 11 hr
    D - 5 hrs
    OFF - 30 min
    D - 4
    W - 30 min
    OFF - 1 hr
    D - 3 hrs
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))
        Event.objects.create(workStatus='W', duration=timedelta(hours=2, minutes=15))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=45))
        Event.objects.create(workStatus='D', duration=timedelta(hours=8, minutes=1))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=11))
        Event.objects.create(workStatus='D', duration=timedelta(hours=5))
        Event.objects.create(workStatus='OFF', duration=timedelta(minutes=30))
        Event.objects.create(workStatus='D', duration=timedelta(hours=4))
        Event.objects.create(workStatus='W', duration=timedelta(minutes=30))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=1))
        Event.objects.create(workStatus='D', duration=timedelta(hours=3))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='V', timeValue=timedelta(hours=12)),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta(hours=14))
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetClocks16(TestCase):
    """
    Test module for GET clocks API
    Case:
    OFF - 5 hours
    OFF - 6 hours
    """

    def setUp(self) -> None:
        # set up environment
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=5))
        Event.objects.create(workStatus='OFF', duration=timedelta(hours=6))

    def test_get_clocks(self):
        # get API response
        response = client.get(reverse('get_clocks'))
        expected = [
            Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta()),
            Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta())
        ]
        serializer = ClockSerializer(expected, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
