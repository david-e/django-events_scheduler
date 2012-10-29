from django.shortcuts import render

import json

import models


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

    
def scheduler_timeline(request):
    """
    This view shows the events scheduler timeline, in which is possible to
    see, edit and delete all events of a specific eventType.
    """
    
    types, events = [], []
    event_types = models.EventType.objects.all()
    # create the left hierarchy of the timeline and list all the events
    for event_type in event_types:
        c, evs = _get_child_and_relative_events(event_type)
        types.append(c)
        events.extend(evs)
    return render(request, 'timeline.html', {
        'etypes': json.dumps(types), 
        'events': json.dumps(events),
    })
