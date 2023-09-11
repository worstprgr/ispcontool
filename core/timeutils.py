#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import datetime as dt
import core.config
import core.exceptions
import core.logger

log = core.logger.Logger(__file__)
cfg = core.config.Interface().config()


class TimeUtils:
    def __init__(self):
        self.ex = core.exceptions.TimeUtilsExc
        self.DAY_HOURS = 24
        self.HOUR_MINUTES = 60
        self.LOWER_BOUNDS = 1
        self.UPPER_BOUNDS = 12, 30
        self.PER_DAY = 'D'
        self.PER_HOUR = 'H'

    def main(self, current_dt: dt.datetime) -> bool:
        """
        Entrypoint of this class.

        :param current_dt: the current datetime, as **datetime object**
        :return: True, if the current minute-value matches a value from the list. False, if not.
        """
        polling_rate = self.set_polling_rate(cfg.TIME_INTERVAL, cfg.TIME_MODE)
        return self.time_check(current_dt, polling_rate, cfg.TIME_TOLERANCE, cfg.TIME_MODE)

    def test_main(self, current_dt: dt.datetime, interval: int, mode: str, tolerance: int) -> bool:
        """
        Entrypoint for the integration test. Without the need of the **config.py** file.

        :param current_dt: the current datetime, as **datetime object**
        :param interval: Only positive integers. Only between 1-12 (if time_mode -> 'D') and 1-30 (if time_mode -> 'H')
        :param mode: 'H' -> per hour or 'D' -> per day
        :param tolerance: n minutes you want to add, to each minute-value
        :return: True, if the current minute-value matches a value from the list. False, if not.
        """
        polling_rate = self.set_polling_rate(interval, mode)
        out = self.time_check(current_dt, polling_rate, tolerance, mode)
        log.this(1, f'method: test_main -> {out}')
        return out

    def set_polling_rate(self, interval: int, time_mode: str) -> list[int, ...]:
        """
        Creates a list with minute-values in a specific interval.
        It basically splits the clock into **n** pieces.
        This method contains two modes:

        - time interval per day -> 'D'
        - time interval per hour -> 'H'

        For example:

        - You want to set the polling rate to 4 times an hour -> interval 4, time_mode: 'H'.
        - You want to set the polling rate to 4 times a day -> interval 4, time_mode: 'D'.

        :param interval: Only positive integers. Only between 1-12 (if time_mode -> 'D') and 1-30 (if time_mode -> 'H')
        :param time_mode: 'H' -> per hour or 'D' -> per day
        :return: a list with the calculated time interval values
        """
        # error handling
        if time_mode == self.PER_DAY and (interval < self.LOWER_BOUNDS or interval > self.UPPER_BOUNDS[0]):
            raise self.ex.IntervalOutOfBounds(self.LOWER_BOUNDS, self.UPPER_BOUNDS[0])
        elif time_mode == self.PER_HOUR and (interval < self.LOWER_BOUNDS or interval > self.UPPER_BOUNDS[1]):
            raise self.ex.IntervalOutOfBounds(self.LOWER_BOUNDS, self.UPPER_BOUNDS[1])
        else:
            # time values for a day or for an hour
            if time_mode == self.PER_DAY:
                return self.divide_clock(self.DAY_HOURS, interval)
            elif time_mode == self.PER_HOUR:
                return self.divide_clock(self.HOUR_MINUTES, interval)
            else:
                raise self.ex.WrongTimeMode

    def divide_clock(self, time_const_type: int, interval: int) -> list[int, ...]:
        """
        It divides a constant time value into **n** parts, and calculates the distance between each part.

        **Caveat:** Since this is a very simple method, it doesn't divide evenly.

        For example: interval 7 @ 24h produces this output:

        **[3, 6, 9, 12, 15, 18, 21]**

        Since these are steps by 3, 00:00 is missing - because the max length if defined by **len(interval)**.

        :param time_const_type: 24 hours or 60 minutes
        :param interval: n minutes
        :return: a list with the calculated time interval values
        """
        if interval <= 0 or type(interval) != int:
            raise self.ex.IsFloatOrZero

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

    def time_check(
            self,
            time_current: dt.datetime,
            time_targets: list[int, ...],
            tolerance_minutes: int,
            time_mode: str
    ) -> bool:
        """
        Compares the current minute-value with the minute-value inside a list.
        Additionally, it adds to each minute-value a tolerance of n minutes.

        :param time_current: current time as **datetime.datetime** object
        :param time_targets: a list with minute-values to compare, with the current time
        :param tolerance_minutes: n minutes you want to add, to each minute-value
        :param time_mode: two modes -> 'D' for per day or 'H' for per hour
        :return: True, if the current minute-value matches a value from the list. False, if not.
        """
        #
        # Error Handling
        #

        # Case: "time_current" got the wrong type
        if not type(time_current) == dt.datetime:
            raise self.ex.WrongType

        # Case: "time_targets" is an invalid list (begins with zero and is greater than 1)
        if len(time_targets) > 1 and time_targets[0] == 0:
            raise self.ex.ListInvalid

        # Case: "time_targets" is a list of [0] and the tolerance exceeds a constant
        if len(time_targets) == 1 and time_targets[0] == 0 and tolerance_minutes >= self.HOUR_MINUTES:
            raise self.ex.MinutesOutOfBounds(tolerance_minutes, self.HOUR_MINUTES)

        # Case: "tolerance_minutes" is zero, negative or a float type
        if tolerance_minutes <= 0 or type(tolerance_minutes) != int:
            raise self.ex.IsFloatOrZero

        # Case: "tolerance_minutes" is exceeding a constant
        if time_mode == self.PER_DAY and tolerance_minutes >= self.HOUR_MINUTES:
            raise self.ex.MinutesOutOfBounds(tolerance_minutes, self.HOUR_MINUTES)

        # Case: "tolerance_minutes" overlaps with the interval values from "time_targets"
        if time_mode == self.PER_HOUR and time_targets[0] != 0 and tolerance_minutes >= time_targets[0]:
            raise self.ex.MinutesOutOfBounds(tolerance_minutes, time_targets[0])

        #
        # Helper Functions
        #

        def tolerance_list_for_hours(initial_list: list[int, ...], tolerance: int) -> list[[int, int], ...]:
            """
            Adds a specific tolerance value to an item in a list.
            This function is specific for the time_mode = 'D'.
            Since an action is made at every hour, the initial minute is zero.

            :param initial_list: a list you want to extend with the tolerance value
            :param tolerance: the desired tolerance you want to add
            :return: a nested list, with the initial minute-value and the modified value
            """
            tolerances = []
            for x in range(len(initial_list)):
                tolerances.append([0, tolerance])
            return tolerances

        def tolerance_list_for_minutes(initial_list: list[int, ...], tolerance: int) -> list[[int, int], ...]:
            """
            Adds a specific tolerance value to an item in a list.

            :param initial_list: a list you want to extend with the tolerance value
            :param tolerance: the desired tolerance you want to add
            :return: a nested list, with the initial minute-value and the modified value
            """
            tolerances = []
            for x in initial_list:
                tolerances.append([x, x + tolerance])
            return tolerances

        def cmp_tolerance(cur_minute: int, cmp_list: list[[int, int], ...]) -> bool:
            """
            Compares the current minute-value with the tolerance values.
            If one condition is true, the whole function returns True.

            :param cur_minute: the current minute-value to compare
            :param cmp_list: a nested list which contains the minimum & maximum value
            :return: True, if one condition is true
            """
            bool_collector: list[bool, ...] = []
            for x in cmp_list:
                if x[0] <= cur_minute <= x[1]:
                    bool_collector.append(True)
                else:
                    bool_collector.append(False)
            if True in bool_collector:
                return True
            else:
                return False

        #
        # Logic
        #

        # time constants
        CURRENT_HOUR: int = time_current.hour
        CURRENT_MINUTE: int = time_current.minute

        # extend the "time_targets" list with the tolerance value
        if time_mode == self.PER_DAY:
            CMP_TIME_LIST: list[[int, int], ...] = tolerance_list_for_hours(time_targets, tolerance_minutes)
            if CURRENT_HOUR in time_targets \
                    and cmp_tolerance(CURRENT_MINUTE, CMP_TIME_LIST):
                return True
            else:
                return False
        elif time_mode == self.PER_HOUR:
            CMP_TIME_LIST: list[[int, int], ...] = tolerance_list_for_minutes(time_targets, tolerance_minutes)
            if cmp_tolerance(CURRENT_MINUTE, CMP_TIME_LIST):
                return True
            else:
                return False
        else:
            raise self.ex.UnknownType
