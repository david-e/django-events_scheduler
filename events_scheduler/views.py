from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import json

import models
from timeline_params import COLORS, TIMELINE_VIEWS_PARAMS


DATETIME_FORMAT = '%Y-%m-%d %H:%M'


def _event2js(ev, section_id):
    """
    Convert an event instance in a javascript dictionary, ready
    for the timeline scheduler.
    """
    return {
        'pk': ev.pk,
        'section_id': section_id,
        'text': ev.name,
        'start_date': ev.start.strftime(DATETIME_FORMAT),
        'end_date': ev.end.strftime(DATETIME_FORMAT),
        'color': ev.background_color,
        'textColor': ev.text_color,
    }


def _get_child_and_relative_events(event_type):
    """
    Collect all the available resources of type event_type and 
    collect all the events relative to theese resources.
    """
    events = []
    key = '%s' % event_type.id
    label = event_type.name
    children = {}
    # create an entry in the resources list for all event_type.content_type objects
    for o in event_type.content_type.get_all_objects_for_this_type():
        # ekey will be the section_id for a row in the scheduler
        ekey = '%s.%s' % (key, o.id) 
        if ekey not in children.keys():
            children[ekey] = {'key': ekey, 'label': '%s' % o}
        # append all the events
        # FIXME: list only the events in the visible range, not all.
        for e in event_type.event_set.filter(object_id=o.id):
            events.append(_event2js(e, ekey))
    child = {'label': event_type.name, 'key': key, "open": True,
             'children': children.values(), 'readonly': event_type.readonly}
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
    """
    Manage the server-side part of insert, update, delete operations.
    The client-side part is managed by a DataProcessor instance variable.
    """
    # ensure that data was sent by post
    if not request.method == 'POST':
        raise Http404

    VALID_OPERATIONS = ['inserted', 'deleted', 'updated']
    
    d, data = request.POST, {}
    tmp_id = d['ids']
    data['start'] = datetime.strptime(d['%s_start_date' % tmp_id], 
                                           DATETIME_FORMAT)
    data['end'] = datetime.strptime(d['%s_end_date' % tmp_id], 
                                         DATETIME_FORMAT)
    data['name'] = d['%s_text' % tmp_id]
    # section_id is in the form '%s.%s' % (event.typology.id, event.object_id)
    section_id = d['%s_section_id' % tmp_id]
    typology_id, data['object_id'] = section_id.split('.')
    data['typology'] = models.EventType.objects.get(id=typology_id)
    # prevent modifications to events of readonly type
    if data['typology'].readonly:
        return HttpResponse(json.dumps({}), 
                            mimetype='text/javascript')
    # !nativeeditor_status could be: inserted, deleted, updated
    operation = d['%s_!nativeeditor_status' % tmp_id]
    if operation not in VALID_OPERATIONS:
        # return an empty response, if we return an error
        # the client-side data_processor stops to handle further operations
        raise HttpResponse()
    if operation == 'inserted':
        ev = models.Event.objects.create(**data)
    else:
        ev_pk = d['%s_pk' % tmp_id]
        ev = models.Event.objects.get(pk=ev_pk)
        if operation == 'deleted':
            ev.delete()
        elif operation == 'updated':
            for field in data.keys():
                setattr(ev, field, data[field])
            ev.save()        
    return HttpResponse(json.dumps(_event2js(ev, section_id)), 
                                   mimetype='text/javascript')
