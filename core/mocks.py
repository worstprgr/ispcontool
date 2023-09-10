#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import random
import core.logger

log = core.logger.Logger(__file__)


class Mocks:
    def __init__(self):
        self.TEST_HOSTS_ON: list[str, ...] = [
            'test.on', 'test.on', 'test.on'
        ]
        self.TEST_HOSTS_OFF: list[str, ...] = [
            'test.off', 'test.off', 'test.off'
        ]

    def sim_hosts_status(self) -> list[str, ...]:
        rnd: int = random.randint(1, 10)
        if rnd % 2 == 0:
            log.this(1, 'Mock: Hosts online')
            return self.TEST_HOSTS_ON
        else:
            log.this(1, 'Mock: Hosts OFFLINE')
            return self.TEST_HOSTS_OFF

    def sim_hosts_n_offline(self, times_offline: int, times_online=1) -> list[list[str, ...], ...]:
        offline_hosts = [self.TEST_HOSTS_OFF] * times_offline
        online_hosts = [self.TEST_HOSTS_ON] * times_online
        return offline_hosts + online_hosts
