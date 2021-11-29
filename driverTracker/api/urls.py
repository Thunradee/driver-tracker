"""
Author: Gift Tangsupakij
Date: 11/24/2021
Description: Routing URL patterns to the view functions
"""

from django.urls import path
from .views import get_post_events, get_update_delete_event, get_clocks

urlpatterns = [
    path('v1/events/', get_post_events, name='get_post_events'),
    path('v1/events/<int:pk>/', get_update_delete_event, name='get_update_delete_event'),
    path('v1/clocks/', get_clocks, name='get_clocks'),
]
