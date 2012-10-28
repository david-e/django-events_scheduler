from django.core.exceptions import ValidationError
from django.test import TestCase

import models


class EventTest(TestCase):
    def setUp(self):
        """
        Create an event with the end before the start
        """
        from datetime import datetime, timedelta
        now = datetime.now()
        # should raise an exception because end must be after
        # the start
        self.ev1 = models.Event(
            name='Ev 1', typology=models.EventType(name='EvType 1'),
            start=now, end=now)
        self.ev2 =   models.Event(
            name='Ev 2', typology=models.EventType(name='EvType 1'),
            start=now + timedelta(days=1), end=now)

        def test_event_start_before_end(self):
            for ev in [self.ev1, self.ev2]:
                with self.assertRaises(ValidationError):
                    ev.clean()
