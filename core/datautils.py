#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import datetime as dt


class DataUtils:
    @staticmethod
    def calc_timedelta(initial_time: dt.datetime, end_time: dt.datetime) -> dt.datetime:
        return end_time.replace(microsecond=0) - initial_time.replace(microsecond=0)

    def data_to_csv(self, initial_time: dt.datetime, end_time: dt.datetime) -> str:
        csv_date = initial_time.date()
        csv_start_time = initial_time.replace(microsecond=0).time()
        csv_end_time = end_time.replace(microsecond=0).time()
        csv_delta = self.calc_timedelta(initial_time, end_time)
        return f'{csv_date},{csv_start_time},{csv_end_time},{csv_delta}'
