from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json

import models
from timeline_params import TIMELINE_VIEWS_PARAMS


def _get_child_and_relative_events(event_type):
    DATETIME_FORMAT = '%Y-%m-%d %H:%M'
    events = []
    key = '%s' % event_type.id
    label = event_type.name
    children = {}
    # create an entry in the resources list for all event_type.content_type objects
    for o in event_type.content_type.get_all_objects_for_this_type():
        ekey = '%s.%s' % (key, o.id) 
        if ekey not in children.keys():
            children[ekey] = {'key': ekey, 'label': '%s' % o}
        # append all the events
        # FIXME: list only the events in the visible range, not all.
        for e in event_type.event_set.filter(object_id=o.id):
            events.append({
                'section_id': ekey, 
                'text': e.name, 
                'start_date': e.start.strftime(DATETIME_FORMAT),
                'end_date': e.end.strftime(DATETIME_FORMAT),
            })
    child = {'label': event_type.name, 'key': key, "open": True, 
             'children': children.values()}
    return child, events

    
def scheduler_timeline(request, view):
    """
    This view shows the events scheduler timeline, in which is possible to
    see, edit and delete all events of a specific eventType.
    """
    if view not in TIMELINE_VIEWS_PARAMS.keys():
        raise Http404
    types, events = [], []
    event_types = models.EventType.objects.all()
    # create the left hierarchy of the timeline and list all the events
    for event_type in event_types:
        c, evs = _get_child_and_relative_events(event_type)
        types.append(c)
        events.extend(evs)
    return render(request, 'events_scheduler/timeline.html', {
        'types': json.dumps(types), 
        'events': json.dumps(events),
        'PARAMS': TIMELINE_VIEWS_PARAMS[view],
    })


@csrf_exempt
def data_processor(request):
    import ipdb; ipdb.set_trace()
    raise Http404
