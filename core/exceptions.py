#!/usr/bin/env python 
# -*- coding:utf-8 -*-

class TimeUtilsExc:
    class TooManyParams(Exception):
        """
        Exception description.
        """
        def __init__(self):
            self.message = 'You can not use the params "per_day" ' \
                           'and "per_hour" at the same time.'
            super().__init__(self.message)

    class IntervalLowerBound(Exception):
        """
        Exception description.
        """
        def __init__(self, lb: int, ub: int):
            self.message = f'Please choose a number between {lb}-{ub}'
            super().__init__(self.message)

    class MissingTimeType(Exception):
        """
        Exception description.
        """
        def __init__(self):
            self.message = 'Missing time type in params'
            super().__init__(self.message)
