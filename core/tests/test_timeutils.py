"""
Had to use a hack, to inject the **core** folder to the sys.path.
Although the module **sysextend** isn't in use, it still imports the
whole content.
"""
import sysextend
import unittest
import datetime
import core.timeutils
import core.exceptions
import core.logger
import core.config

log = core.logger.Logger(__file__)
log.file_save = False
dt = datetime.datetime
t = core.timeutils.TimeUtils()
ex = core.exceptions.TimeUtilsExc()


class TestTimeutils(unittest.TestCase):
    def test_set_polling_rate_custom_exceptions(self):
        # GIVEN
        time_mode = 'D'
        wrong_time_mode = 'Q'
        input_valid1 = 1
        input_invalid1 = '123'
        input_invalid2 = 'test'

        # THEN
        with self.assertRaises(ex.WrongTimeMode):
            t.set_polling_rate(input_valid1, wrong_time_mode)

        with self.assertRaises(TypeError):
            t.set_polling_rate(input_invalid1, time_mode)

        with self.assertRaises(TypeError):
            t.set_polling_rate(input_invalid2, time_mode)

    def test_set_polling_rate_times_per_day(self):
        # GIVEN
        time_mode = 'D'
        input_valid1 = 1
        input_valid2 = 4
        input_valid3 = 12
        scenario1_truth = [0]
        scenario2_truth = [6, 12, 18, 0]
        scenario3_truth = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 0]

        input_invalid1 = 15
        input_invalid2 = -1
        input_invalid3 = 0

        # WHEN
        scenario1 = t.set_polling_rate(input_valid1, time_mode)
        scenario2 = t.set_polling_rate(input_valid2, time_mode)
        scenario3 = t.set_polling_rate(input_valid3, time_mode)

        # THEN
        self.assertEqual(scenario1_truth, scenario1)
        self.assertEqual(scenario2_truth, scenario2)
        self.assertEqual(scenario3_truth, scenario3)

        with self.assertRaises(ex.IntervalOutOfBounds):
            t.set_polling_rate(input_invalid1, time_mode)

        with self.assertRaises(ex.IntervalOutOfBounds):
            t.set_polling_rate(input_invalid2, time_mode)

        with self.assertRaises(ex.IntervalOutOfBounds):
            t.set_polling_rate(input_invalid3, time_mode)

    def test_set_polling_rate_times_per_hour(self):
        # GIVEN
        time_mode = 'H'
        input_valid1 = 1
        input_valid2 = 4
        input_valid3 = 30
        scenario1_truth = [0]
        scenario2_truth = [15, 30, 45, 0]
        scenario3_truth = [
            2, 4, 6, 8, 10, 12, 14, 16,
            18, 20, 22, 24, 26, 28, 30,
            32, 34, 36, 38, 40, 42, 44,
            46, 48, 50, 52, 54, 56, 58,
            0
        ]

        input_invalid1 = 35
        input_invalid2 = -1
        input_invalid3 = 0

        # WHEN
        scenario1 = t.set_polling_rate(input_valid1, time_mode)
        scenario2 = t.set_polling_rate(input_valid2, time_mode)
        scenario3 = t.set_polling_rate(input_valid3, time_mode)

        # THEN
        self.assertEqual(scenario1_truth, scenario1)
        self.assertEqual(scenario2_truth, scenario2)
        self.assertEqual(scenario3_truth, scenario3)

        with self.assertRaises(ex.IntervalOutOfBounds):
            t.set_polling_rate(input_invalid1, time_mode)

        with self.assertRaises(ex.IntervalOutOfBounds):
            t.set_polling_rate(input_invalid2, time_mode)

        with self.assertRaises(ex.IntervalOutOfBounds):
            t.set_polling_rate(input_invalid3, time_mode)

    def test_divide_clock_exceptions(self):
        # GIVEN
        CONST_FULL_DAY_HOURS = 24
        invalid_interval1 = -1
        invalid_interval2 = 5.55
        invalid_interval3 = 0

        # THEN
        with self.assertRaises(ex.IsFloatOrZero):
            t.divide_clock(CONST_FULL_DAY_HOURS, invalid_interval1)

        with self.assertRaises(ex.IsFloatOrZero):
            t.divide_clock(CONST_FULL_DAY_HOURS, invalid_interval2)

        with self.assertRaises(ex.IsFloatOrZero):
            t.divide_clock(CONST_FULL_DAY_HOURS, invalid_interval3)

    def test_divide_clock_day(self):
        # GIVEN
        CONST_FULL_DAY_HOURS = 24
        valid_interval1 = 1
        valid_interval2 = 3
        valid_interval3 = 10

        scenario1_truth = [0]
        scenario2_truth = [8, 16, 0]
        scenario3_truth = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

        # WHEN
        scenario1 = t.divide_clock(CONST_FULL_DAY_HOURS, valid_interval1)
        scenario2 = t.divide_clock(CONST_FULL_DAY_HOURS, valid_interval2)
        scenario3 = t.divide_clock(CONST_FULL_DAY_HOURS, valid_interval3)

        # THEN
        self.assertEqual(scenario1_truth, scenario1)
        self.assertEqual(scenario2_truth, scenario2)
        self.assertEqual(scenario3_truth, scenario3)

    def test_divide_clock_hour(self):
        # GIVEN
        CONST_FULL_HOUR_MINUTES = 60

        valid_interval1 = 1
        valid_interval2 = 3
        valid_interval3 = 10

        scenario1_truth = [0]
        scenario2_truth = [20, 40, 0]
        scenario3_truth = [6, 12, 18, 24, 30, 36, 42, 48, 54, 0]

        # WHEN
        scenario1 = t.divide_clock(CONST_FULL_HOUR_MINUTES, valid_interval1)
        scenario2 = t.divide_clock(CONST_FULL_HOUR_MINUTES, valid_interval2)
        scenario3 = t.divide_clock(CONST_FULL_HOUR_MINUTES, valid_interval3)

        # THEN
        self.assertEqual(scenario1_truth, scenario1)
        self.assertEqual(scenario2_truth, scenario2)
        self.assertEqual(scenario3_truth, scenario3)

    def test_time_check_exceptions(self):
        # GIVEN
        dummy_list = []
        valid_list = [0]
        invalid_list = [0, 1]

        dummy_int = 0
        invalid_int1 = 5.33
        invalid_int2 = -1
        invalid_int3 = 60

        dummy_mode = ''

        valid_time1 = dt(2023, 9, 3, 4, 1, 0)  # 2023-09-03 04:01:00
        invalid_time1 = '2023-09-03 04:01:00'
        invalid_time2 = 20230903

        # THEN
        with self.assertRaises(ex.WrongType):
            t.time_check(invalid_time1, dummy_list, dummy_int, dummy_mode)

        with self.assertRaises(ex.WrongType):
            t.time_check(invalid_time2, dummy_list, dummy_int, dummy_mode)

        with self.assertRaises(ex.ListInvalid):
            t.time_check(valid_time1, invalid_list, dummy_int, dummy_mode)

        with self.assertRaises(ex.MinutesOutOfBounds):
            t.time_check(valid_time1, valid_list, invalid_int3, dummy_mode)

        with self.assertRaises(ex.IsFloatOrZero):
            t.time_check(valid_time1, dummy_list, invalid_int1, dummy_mode)

        with self.assertRaises(ex.IsFloatOrZero):
            t.time_check(valid_time1, dummy_list, invalid_int2, dummy_mode)

    def test_time_check_day(self):
        # GIVEN
        valid_list = [4, 8, 12, 16, 18, 22]
        valid_int = 12  # minutes
        invalid_int1 = 60
        invalid_int2 = 70
        set_mode = 'D'

        valid_time1 = dt(2023, 9, 3, 4, 1, 0)  # 2023-09-03 04:01:00
        valid_time2 = dt(2020, 9, 3, 4, 11, 55)  # 2020-09-03 04:11:55
        invalid_time1 = dt(2023, 9, 3, 5, 0, 00)  # 2023-09-03 05:00:00
        invalid_time2 = dt(2020, 9, 3, 5, 0, 16)  # 2020-09-03 05:00:16

        # WHEN
        scenario1 = t.time_check(valid_time1, valid_list, valid_int, set_mode)
        scenario2 = t.time_check(valid_time2, valid_list, valid_int, set_mode)
        scenario3 = t.time_check(invalid_time1, valid_list, valid_int, set_mode)
        scenario4 = t.time_check(invalid_time2, valid_list, valid_int, set_mode)

        # THEN
        self.assertEqual(True, scenario1)
        self.assertEqual(True, scenario2)
        self.assertEqual(False, scenario3)
        self.assertEqual(False, scenario4)

        with self.assertRaises(ex.MinutesOutOfBounds):
            t.time_check(valid_time1, valid_list, invalid_int1, set_mode)

        with self.assertRaises(ex.MinutesOutOfBounds):
            t.time_check(valid_time1, valid_list, invalid_int2, set_mode)

    def test_time_check_hour(self):
        # GIVEN
        valid_list = [15, 30, 45, 0]
        valid_int = 5  # minutes
        invalid_int1 = 15
        invalid_int2 = 20
        set_mode = 'H'

        valid_time1 = dt(2023, 9, 3, 4, 15, 0)  # 2023-09-03 04:15:00
        valid_time2 = dt(2020, 9, 3, 4, 17, 55)  # 2020-09-03 04:17:55
        invalid_time1 = dt(2023, 9, 3, 5, 14, 00)  # 2023-09-03 05:14:00
        invalid_time2 = dt(2020, 9, 3, 5, 29, 16)  # 2020-09-03 05:29:16

        # WHEN
        scenario1 = t.time_check(valid_time1, valid_list, valid_int, set_mode)
        scenario2 = t.time_check(valid_time2, valid_list, valid_int, set_mode)
        scenario3 = t.time_check(invalid_time1, valid_list, valid_int, set_mode)
        scenario4 = t.time_check(invalid_time2, valid_list, valid_int, set_mode)

        # THEN
        self.assertEqual(True, scenario1)
        self.assertEqual(True, scenario2)
        self.assertEqual(False, scenario3)
        self.assertEqual(False, scenario4)

        with self.assertRaises(ex.MinutesOutOfBounds):
            t.time_check(valid_time1, valid_list, invalid_int1, set_mode)

        with self.assertRaises(ex.MinutesOutOfBounds):
            t.time_check(valid_time1, valid_list, invalid_int2, set_mode)

    def test_main(self):
        # GIVEN
        valid_dt = dt(2023, 9, 1, 4, 15, 0)
        invalid_dt = dt(2023, 9, 1, 4, 14, 0)
        valid_interval = 4
        valid_mode = 'H'
        valid_tolerance = 5

        # WHEN
        scenario1 = t.test_main(valid_dt, valid_interval, valid_mode, valid_tolerance)
        scenario2 = t.test_main(invalid_dt, valid_interval, valid_mode, valid_tolerance)

        # THEN
        self.assertEqual(True, scenario1)
        self.assertEqual(False, scenario2)


if __name__ == '__main__':
    unittest.main()
