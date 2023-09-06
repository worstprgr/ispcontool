#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import datetime as dt
import time
from core.exceptions import TimeUtilsExc


date1 = dt.time(14, 50, 0)
date2 = dt.time(15, 0, 0)


def set_polling_rate(interval: int, per_day=False, per_hour=False) -> list[int]:
    # constants
    DAY_HOURS = 24
    HOUR_MINUTES = 60
    LOWER_BOUNDS = 1
    UPPER_BOUNDS = 12

    # error handling
    # if interval < LOWER_BOUNDS or interval > UPPER_BOUNDS:
    #     raise TimeUtilsExc.IntervalLowerBound(LOWER_BOUNDS, UPPER_BOUNDS)

    if per_day and per_hour:
        raise TimeUtilsExc.TooManyParams

    # time values for a day or for an hour
    if per_day:
        return divide_clock(DAY_HOURS, interval)
    elif per_hour:
        return divide_clock(HOUR_MINUTES, interval)
    else:
        raise TimeUtilsExc.MissingTimeType


def divide_clock(time_const_type: int, interval: int) -> list[int]:
    # init
    time_store: list[int] = []
    time_value: int = 0
    time_increment: int = round(time_const_type / interval)

    for x in range(interval):
        time_value += time_increment
        if time_value >= time_const_type:
            time_value = time_value - time_const_type
        time_store.append(time_value)
    return time_store


def time_check(current_time: int, time_lbound: int, time_ubound: int) -> bool:
    if time_lbound <= current_time <= time_ubound:
        return True
    else:
        return False


def routine():
    polling_rate = 2
    routine_locked = False
    while True:
        now = dt.datetime.now()
        print('Stuff')
        time.sleep(polling_rate)


if __name__ == '__main__':
    # print(int(dt.datetime.now().strftime('%M')))
    t = set_polling_rate(45, per_hour=True)
    print(t)
    # print(time_check(6, 5, 7))
