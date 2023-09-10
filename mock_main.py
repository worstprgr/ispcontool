#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import time
from datetime import datetime as dt
from core import signalutils
from core import timeutils
from core import fileutils
from core import portutils
from core import datautils
from core import mocks


class MockMain:
    """
    Mock Routine
    """
    def __init__(self):
        self.port_utl = portutils.PortUtils()
        self.file_utl = fileutils.FileUtils()
        self.time_utl = timeutils.TimeUtils()
        self.sig_utl = signalutils.Terminate()
        self.data_utl = datautils.DataUtils()
        self.mocks = mocks.Mocks()
        # Test Data
        self.main_routine_sleep = 1
        self.sub_routine_sleep = 1
        self.time_interval = 4
        self.time_mode = 'H'
        self.time_tolerance = 5
        # Config
        self.write_to_file = False

    def main_routine(self):
        while not self.sig_utl.term_status:
            CURRENT_TIME = dt(2023, 9, 10, 3, 15)  # 2023-09-10 03:15:00

            # 1. Question: Is it the right time?
            cp_time = self.time_utl.test_main(CURRENT_TIME, self.time_interval, self.time_mode, self.time_tolerance)

            if cp_time:
                # 2. Question: Is one of the hosts offline?
                hosts_online: bool = self.port_utl.con_check(self.mocks.sim_hosts_status(), test=True)
                print('Main Routine: Status:', hosts_online, '\n')

                if not hosts_online:
                    # 3. Fact: Hosts are offline
                    self.sub_routine()
            self.sig_utl.sleep(self.main_routine_sleep)

    def sub_routine(self):
        # 4. Action: Get the initial time
        INITIAL_TIME: object = dt.now()
        MOCK_COUNTER: int = 0
        while not self.sig_utl.term_status:
            # 5. Question: Are the hosts still offline?
            #       Mock: Loop n times through offline hosts
            hosts_online: bool = self.port_utl.con_check(self.mocks.sim_hosts_n_offline(3)[MOCK_COUNTER], test=True)
            MOCK_COUNTER += 1
            print('Sub Routine: Status:', hosts_online)

            if hosts_online:
                # 6. Action: Get the end time and write to file
                ONLINE_TIME: object = dt.now()
                csv_out = self.data_utl.data_to_csv(INITIAL_TIME, ONLINE_TIME)
                if self.write_to_file:
                    self.file_utl.write_to_csv(csv_out)
                print('CSV\t', csv_out)
                break
            self.sig_utl.sleep(self.sub_routine_sleep)


if __name__ == '__main__':
    m = MockMain()
    m.main_routine()
