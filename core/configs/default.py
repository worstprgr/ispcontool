#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import core.logger
import os

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
        self.TIME_INTERVAL = 4  # n times
        self.TIME_MODE = 'H'  # D -> per day / H -> per hour
        self.TIME_TOLERANCE = 5  # minutes

        #
        # Routine config
        #
        self.MAIN_ROUTINE_SLEEP: int = 60  # seconds
        self.SUB_ROUTINE_SLEEP: int = 60  # seconds
        self.SUB_RATE: int = 1  # seconds (Default 1)
