#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from datetime import datetime as dt
from core import signalutils as stl
from core import timeutils as ttl
from core import fileutils as ftl
from core import config as cfg
from core import portutils as ptl


class Main:
    def __init__(self):
        self.ptl = ptl.PortUtils()
        self.ftl = ftl.FileUtils()
        self.ttl = ttl.TimeUtils()
        self.sigterm = stl.Terminate()
        self.mroutine_timer: int = 1
        self.sroutine_timer: int = 1

    def main_routine(self):
        while not self.sigterm.term_status:
            status: bool = self.ptl.con_check(cfg.HOSTS)
            print('Main Routine: Status:', status, '\n')
            self.sub_routine(status)
            self.ttl.set_timer(self.mroutine_timer)

    def sub_routine(self, status):
        if not status:
            initial_dt: object = dt.now()
            while not self.sigterm.term_status:
                status_sub_loop: bool = self.ptl.con_check(cfg.HOSTS)
                print('Sub Routine: Status:', status_sub_loop)
                if status_sub_loop:
                    dt_delta = self.ttl.calc_dt_delta(initial_dt)
                    self.ftl.write_to_csv(cfg.CSV_ENTRY(initial_dt, dt_delta[0], dt_delta[1]))
                    print('CSV\t', (initial_dt, dt_delta[0], dt_delta[1]))
                    break
                self.ttl.set_timer(self.sroutine_timer)


if __name__ == '__main__':
    #m = Main()
    #m.main_routine()
    print('Main')
