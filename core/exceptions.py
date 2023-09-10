#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import core.logger

log = core.logger.Logger(__file__)


class TimeUtilsExc:
    class IntervalOutOfBounds(Exception):
        def __init__(self, lb: int, ub: int):
            self.message = f'Value Out of Bounds: Please choose a integer between {lb}-{ub}'
            log.this(3, self.message)
            super().__init__(self.message)

    class IsFloatOrZero(Exception):
        def __init__(self):
            self.message = 'Invalid Integer: Please choose an unsigned integer'
            log.this(3, self.message)
            super().__init__(self.message)

    class WrongTimeMode(Exception):
        def __init__(self):
            self.message = 'Missing Time Mode in Params: Use "D" or "H" for checking every n hour or every n minute'
            log.this(3, self.message)
            super().__init__(self.message)

    class WrongType(Exception):
        def __init__(self):
            self.message = 'Wrong Input Type: Please use the "datetime.datetime" object'
            log.this(3, self.message)
            super().__init__(self.message)

    class UnknownType(Exception):
        def __init__(self):
            self.message = 'Unknown Input Type: Use "D" or "H" for checking every n hour or every n minute'
            log.this(3, self.message)
            super().__init__(self.message)

    class MinutesOutOfBounds(Exception):
        def __init__(self, curr_min: int, max_min: int):
            self.message = f'Value Out of Bounds: Maximum allowed value is "{max_min-1}". Your value is "{curr_min}"'
            log.this(3, self.message)
            super().__init__(self.message)

    class ListInvalid(Exception):
        def __init__(self):
            self.message = 'Invalid List: The list begins with "zero" and is greater than 1 item.'
            log.this(4, self.message)
            super().__init__(self.message)


class SignalUtilsExc:
    class BelowSubRate(Exception):
        def __init__(self):
            self.message = 'Integer Mismatch: "time_seconds" is smaller than "sub_rate", please adjust the sub rate.'
            log.this(3, self.message)
            super().__init__(self.message)
