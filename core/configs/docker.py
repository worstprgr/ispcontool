#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import core.logger

log = core.logger.Logger(__file__)


class Conf:
    def __init__(self):
        #
        # CSV
        #
        """
        File name format will be:
           isp_connectivity-report_2023.csv
        """
        self.CSV_FILENAME_PREFIX: str = 'isp'
        self.CSV_FILENAME_MID: str = 'connectivity-report'
        self.CSV_FILE_EXTENSION: str = 'csv'
        self.CSV_HEADER: str = 'START,END,DURATION'

        #
        # Polling rates & interval
        #
        self.TIME_INTERVAL: int = int(os.environ['TIME_INTERVAL'])  # n times
        self.TIME_MODE: str = os.environ['TIME_MODE']  # D -> per day / H -> per hour
        self.TIME_TOLERANCE: int = int(os.environ['TIME_TOLERANCE'])  # minutes

        #
        # Routine config
        #
        self.MAIN_ROUTINE_SLEEP: int = int(os.environ['MAIN_ROUTINE_SLEEP'])  # seconds
        self.SUB_ROUTINE_SLEEP: int = int(os.environ['SUB_ROUTINE_SLEEP'])  # seconds
        self.SUB_RATE: int = int(os.environ['SUB_RATE'])  # seconds (Default 1)
