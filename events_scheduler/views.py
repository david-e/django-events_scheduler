from django.http import Http404
from django.shortcuts import render

import json

import models

# d=Day, w=Week and m=Month 
TIMELINE_VIEWS = {
    'd': {
        'x_unit': 'minute',
        'x_date': "%H:%i",
        'x_step': 60,
        'x_size': 17,     # from 7:00 to 24:00 
        'x_start': 7,    # from 7:00
        'x_length': 48,
        'event_dy': 'full',
        'second_scale': {'x_unit': 'day', 'x_date': '%l'}
    },
    'w': {
         'x_unit': 'day',
        'x_date': "%D, %d",
        'x_step': 1,
        'x_size': 6,     # from monday to saturday
        'x_start': 0,    # from monday
        'x_length': 48,
        'event_dy': 'full',
        'second_scale': {'x_unit': 'month', 'x_date': '%F'}
    },
    'm': {
         'x_unit': 'day',
        'x_date': "%d",
        'x_step': 1,
        'x_size': 31,     # one month
        'x_start': 0,    # from the first day
        'x_length': 48,
        'event_dy': 'full',
        'second_scale': {'x_unit': 'day', 'x_date': '%D'}
    },
    'q': {
         'x_unit': 'week',
        'x_date': "%D, %d",
        'x_step': 1,
        'x_size': 12,     # one month
        'x_start': 0,    # from the first day
        'x_length': 48,
        'event_dy': 'full',
        'second_scale': {'x_unit': 'month', 'x_date': '%F'}
    },
}


def _get_child_and_relative_events(event_type):
    # FIXME: list only the events in the visible range, not all.
    DATETIME_FORMAT = '%Y-%m-%d %H:%M'
    events = []
    key = str(event_type.id)
    label = event_type.name
    children = {}
    for e in event_type.event_set.all():
        ekey = '%s.%s' % (key, e.object_id) 
        if ekey not in children.keys():
            children[ekey] = {'key': ekey, 'label': '%s' % e.related_object()}
        events.append({
            'section_id': ekey, 
            'text': e.name, 
            'start_date': e.start.strftime(DATETIME_FORMAT),
            'end_date': e.end.strftime(DATETIME_FORMAT),
        })
    child = {'label': event_type.name, 'key': ekey, "open": True, 
             'children': children.values()}
    return child, events

    
def scheduler_timeline(request, view):
    """
    This view shows the events scheduler timeline, in which is possible to
    see, edit and delete all events of a specific eventType.
    """
    if view not in TIMELINE_VIEWS.keys():
        raise Http404
    types, events = [], []
    event_types = models.EventType.objects.all()
    # create the left hierarchy of the timeline and list all the events
    for event_type in event_types:
        c, evs = _get_child_and_relative_events(event_type)
        types.append(c)
        events.extend(evs)
    return render(request, 'timeline.html', {
        'types': json.dumps(types), 
        'events': json.dumps(events),
        'PARAMS': TIMELINE_VIEWS[view],
    })
