#!/usr/bin/env python 
# -*- coding:utf-8 -*-
from datetime import datetime as dt
from core import signalutils
from core import timeutils
from core import fileutils
from core import portutils
from core import datautils
import core.conutils
import core.config
import core.logger

log = core.logger.Logger(__file__)
cfg = core.config.Interface()


class Main:
    def __init__(self):
        self.port_utl = portutils.PortUtils()
        self.file_utl = fileutils.FileUtils()
        self.time_utl = timeutils.TimeUtils()
        self.sig_utl = signalutils.Terminate()
        self.data_utl = datautils.DataUtils()
        self.is_container: bool = core.conutils.is_container()
        if not self.is_container:
            log.this(1, 'Using Manual Config')
        else:
            log.this(1, 'Using Docker Config')

    def main_routine(self):
        log.this(1, 'Started Main Routine')
        SUB_ROUTINE_LOCKED: bool = False
        while not self.sig_utl.term_status:
            log.this(0, f'Sub Routine Locked: {SUB_ROUTINE_LOCKED}')
            CURRENT_TIME = dt.now()

            # 1. Question: Is it the right time?
            cp_time = self.time_utl.main(CURRENT_TIME)

            if not cp_time:
                SUB_ROUTINE_LOCKED = False
                log.this(1, 'Sub Routine is free')

            if cp_time and not SUB_ROUTINE_LOCKED:
                SUB_ROUTINE_LOCKED = True
                log.this(1, 'Sub Routine is locked')

                # 2. Question: Is one of the hosts offline?
                hosts_online: bool = self.port_utl.con_check(cfg.HOSTS)

                if not hosts_online:
                    # 3. Fact: Hosts are offline
                    self.sub_routine()
            self.sig_utl.sleep(cfg.config().MAIN_ROUTINE_SLEEP)

    def sub_routine(self):
        log.this(1, 'Started Sub Routine')
        # 4. Action: Get the initial time
        INITIAL_TIME: object = dt.now()
        while not self.sig_utl.term_status:
            # 5. Question: Are the hosts still offline?
            hosts_online: bool = self.port_utl.con_check(cfg.HOSTS)

            if hosts_online:
                # 6. Action: Get the end time and write to file
                ONLINE_TIME: object = dt.now()
                csv_out = self.data_utl.data_to_csv(INITIAL_TIME, ONLINE_TIME)
                self.file_utl.write_to_csv(csv_out)
                print('CSV\t', csv_out)
                break
            self.sig_utl.sleep(cfg.config().SUB_ROUTINE_SLEEP, cfg.config().SUB_RATE)


if __name__ == '__main__':
    m = Main()
    m.main_routine()
