from django.shortcuts import render

import models


def scheduler_timeline(request):
    """
    This view shows the events scheduler timeline, in which is possible to
    see, edit and delete all events of a specific eventType.
    """
    return render(request, 'timeline.html')
