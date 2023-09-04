#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import signal


class Terminate:
    """
    If a 'signal interrupt' or a 'signal termination' is received,
    the variable 'term_status' changes its state.

    The variable is used to change the condition of the while-loop
    inside the main.py
    """
    def __init__(self) -> None:
        self.term_status: bool = False
        signal.signal(signal.SIGINT, self.__terminate)
        signal.signal(signal.SIGTERM, self.__terminate)

    def __terminate(self, *args) -> None:
        self.term_status = True
        print('Sigterm: True')
