from django.utils.translation import ugettext_lazy as _

from random import randint


# d=Day, w=Week and m=Month 
TIMELINE_VIEWS_PARAMS = {
    'd': {
        'x_unit': 'minute',
        'x_date': "%H:%i",
        'x_step': 60,
        'x_size': 17,     # from 7:00 to 24:00 
        'x_start': 7,    # from 7:00
        'x_length': 24,
        'event_dy': 'full',
        'second_scale': {'x_unit': 'day', 'x_date': '%l'}
    },
    'w': {
         'x_unit': 'day',
        'x_date': "%D, %d",
        'x_step': 1,
        'x_size': 6,     # from monday to saturday
        'x_start': 0,    # from monday
        'x_length': 6,
        'event_dy': 'full',
        'second_scale': {'x_unit': 'month', 'x_date': '%F'}
    },
    'm': {
         'x_unit': 'day',
        'x_date': "%d",
        'x_step': 1,
        'x_size': 31,     # one month
        'x_start': 0,    # from the first day
        'x_length': 31,
        'event_dy': 'full',
        'second_scale': {'x_unit': 'day', 'x_date': '%D'}
    },
    'q': {
         'x_unit': 'week',
        'x_date': "%D, %d",
        'x_step': 1,
        'x_size': 12,     # one month
        'x_start': 0,    # from the first day
        'x_length': 12,
        'event_dy': 'full',
        'second_scale': {'x_unit': 'month', 'x_date': '%F'}
    },
}

class Colors(object):
    _choices = (
        (('0', _('Black on green')),   ('#00ff88', 'black')), 
        (('1', _('Gray on yellow')),    ('#ffe763', '#b7a543')),
        (('2', _('White on purple')), ('purple', 'white')),       
        (('3', _('White on red')),       ('red', 'white')),         
        (('4', _('White on blue')),     ('blue', 'white')),
    )

    def get_color(self, index=None):
        """
        Return the the index color from the _choices array.
        If index is None or a inexistent value return a random color
        """
        if type(index) in [unicode, str]:
            index = int(index)
        if  index is None:
            index = self._randint()
        return self._choices[index][1]

    def _randint(self):
        return randint(0, len(self._choices)-1)
        
    def pick_choice(self):
        return str(self._randint())
        
    @property
    def choices(self):
        return [c[0] for c in self._choices]

        
COLORS = Colors()
