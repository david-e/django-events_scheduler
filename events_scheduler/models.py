from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from timeline_params import COLORS


class EventType(models.Model):
    """
    This class defines the event type.
    An eventType instance is linked to a ContentType (like auth.user, or
    any other model that defines a resource whose usage needs to
    be scheduled).
    """
    name = models.CharField(_('Type name'), max_length=128,
                            unique=True)
    descr = models.TextField(_('Description'), blank=True)
    content_type = models.ForeignKey(ContentType, 
                                     verbose_name=_('Reference Model'))
    readonly = models.BooleanField(_('Read-only'), default=False)

    class Meta:
        verbose_name = _('Event type')
        verbose_name_plural = _('Event types')
        
    def __unicode__(self):
        return self.name
    

class Event(models.Model):
    """
    The event class is the core of this application.
    """
    name = models.CharField(_('Name'), max_length=128)
    typology = models.ForeignKey(EventType, verbose_name=_('Type'))
    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))
    object_id = models.PositiveIntegerField()
    color = models.CharField(_('Color'), max_length=2, choices=COLORS.choices,
                             default=COLORS.pick_choice)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
    
    def __unicode__(self):
        return self.name

    def clean(self):
        if self.end <= self.start:
            raise ValidationError('End datetime must be after Start')

    def related_object(self):
        return self.typology.content_type.get_object_for_this_type(
            id=self.object_id)

    @property
    def background_color(self):
        return COLORS.get_color(self.color)[0]

    @property
    def text_color(self):
        return COLORS.get_color(self.color)[1]
