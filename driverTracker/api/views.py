"""
Author: Gift Tangsupakij
Date: 11/24/2021
Description: Functions that handle URL requests
"""

from django.http import HttpResponse
from .models import Event, Clock
from .serializers import EventSerializer, ClockSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta


########################################################################
#                              Events                                  #
########################################################################


@api_view(['GET', 'POST'])
def get_post_events(request):
    """ Handles GET and POST of event requests """

    # GET request
    if request.method == 'GET':
        # retrieve event data from the database
        events = Event.objects.all()
        # convert event objects to json data
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    # POST request
    elif request.method == 'POST':
        # convert json data to an event object
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # create and store the event object if it is valid
            # return created data and status
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return error and bad request status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def get_update_delete_event(request, pk):
    """ Handles GET, PUT, DELETE of an event object request """

    try:
        event = Event.objects.get(pk=pk)  # retrieve object from the database
    except Event.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)  # return 404 status if the object does not exist

    # GET request
    if request.method == 'GET':
        # convert json data to an event object
        serializer = EventSerializer(event)
        return Response(serializer.data)

    # PUT request
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)

        if serializer.is_valid():
            serializer.save()  # update the event object if it is valid
            return Response(serializer.data)
        # return error message and 400 status if the object does not exist
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE request
    elif request.method == 'DELETE':
        event.delete()  # delete the event object
        # return 204 status
        return Response(status=status.HTTP_204_NO_CONTENT)


########################################################################
#                               Clocks                                 #
########################################################################


@api_view(['GET'])
def get_clocks(request):
    """ Handles GET event summary request """
    if request.method == 'GET':
        # retrieve events data from the database
        events = Event.objects.all()
        # get event summary (drive clock and work clock)
        clocks = make_clocks(events)
        # covert clock objects to json data
        serializer = ClockSerializer(clocks, many=True)
        return Response(serializer.data)


def make_clocks(events):
    """ Create events summary (drive clock and work clock) """

    # initialize drive and work clocks
    drive_clock = Clock(type='DRIVE_CLOCK', violationStatus='OK', timeValue=timedelta())
    work_clock = Clock(type='WORK_CLOCK', violationStatus='OK', timeValue=timedelta())

    # Find reset clock position (first record after consecutive OFF time that is greater than 10 hours)
    off = timedelta()
    prevStatus = 'W'
    i = 0
    start = 0  # negative of this value is the index of the first record after consecutive OFF time that is greater than 10 hours

    # iterate through the events list from the most recent
    for i, x in enumerate(reversed(events)):
        if x.workStatus == 'OFF':
            off += x.duration
            if prevStatus != 'OFF':
                start = i
            prevStatus = 'OFF'
        else:
            off = timedelta()
            prevStatus = 'W'

        if off > timedelta(hours=10):
            break

    # found reset position as the most recent event, set start to -n
    if off > timedelta(hours=10):
        if start == 0:
            start = -len(events)
    # reset position is not found, set start to 0
    else:
        if i == len(events) - 1:
            start = 0

    # calculate time value for both clocks
    # iterate through the events list starting at first event after 10 hrs consecutive off time
    for x in list(events)[-start:]:
        # add driving time to both clocks
        if x.workStatus == 'D':
            drive_clock.timeValue += x.duration
            work_clock.timeValue += x.duration
        # add working time to work clock
        elif x.workStatus == 'W':
            work_clock.timeValue += x.duration
        # add off-work time to work clock
        elif x.workStatus == 'OFF':
            work_clock.timeValue += x.duration

    # Calculate violation status of drive clock
    if drive_clock.timeValue > timedelta(hours=11):
        drive_clock.violationStatus = 'V'

    # Calculate violation status of work clock
    if work_clock.timeValue > timedelta(hours=14):
        work_clock.violationStatus = 'V'

    # return both clocks
    return [drive_clock, work_clock]
