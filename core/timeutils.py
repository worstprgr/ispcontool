#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import datetime as dt
import time


class TimeUtils:
    @staticmethod
    def set_timer(interval: int) -> None:
        interval_in_seconds = interval * 60
        time.sleep(interval_in_seconds)

    @staticmethod
    def calc_dt_delta(initial_time: object) -> tuple:
        dt_now = dt.datetime.now()
        return dt_now, dt_now - initial_time

    # TODO:
    #   Implement a clock, that gets checked every n seconds
    #   Like in the monitor program


if __name__ == '__main__':
    initial_dt: object = dt.datetime(2023, 9, 3, 4, 1, 0, 11)
    # print('Initial Time:', initial_dt)

    t = TimeUtils()
    print(t.set_timer(2))
