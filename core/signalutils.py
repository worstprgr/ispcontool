#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import signal
import time
import core.exceptions
import core.logger

log = core.logger.Logger(__file__)


class Terminate:
    """
    If a 'signal interrupt' or a 'signal termination' is received,
    the variable 'term_status' changes its state.

    The variable is used to change the condition of the while-loop
    inside the main.py
    """
    def __init__(self):
        self.ex = core.exceptions.SignalUtilsExc
        self.term_status: bool = False
        signal.signal(signal.SIGINT, self.__terminate)
        signal.signal(signal.SIGTERM, self.__terminate)

    def __terminate(self, *args) -> None:
        self.term_status = True
        log.this(1, 'SIGTERM / SIGINT received')

    def sleep(self, time_seconds: int, sub_rate=1) -> None:
        """
        Sleep method, but in a way, SIGTERM & SIGKILL still gets executed.

        :param time_seconds: **int**: how long the sleep should last (in iterations)
        :param sub_rate: **int & float**: how long an iteration should take time (in seconds) (Default: 1)
        :return: None
        """
        # Case: "time_seconds" is below the "sub_rate"
        if time_seconds < sub_rate:
            raise self.ex.BelowSubRate
        for x in range(time_seconds):
            if self.term_status:
                break
            time.sleep(sub_rate)
