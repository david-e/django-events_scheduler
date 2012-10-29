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
