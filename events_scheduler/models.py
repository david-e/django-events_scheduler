from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


class EventType(models.Model):
    """
    This class defines the event type.
    """
    name = models.CharField(_('Type name'), max_length=128,
                            unique=True)
    descr = models.TextField(_('Description'), blank=True)

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

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
    
    def __unicode__(self):
        return self.name

    def clean(self):
        if self.stop <= self.start:
            raise ValidationError('End datetime must be after Start')
