#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import core.configs.default
import core.configs.docker
import core.conutils


class Interface:
    def __init__(self):
        self.is_container: bool = core.conutils.is_container()

        # Hosts to check
        self.HOSTS: list[str, ...] = [
            'google.com',
            'x.com',
            'duckduckgo.com'
        ]

    def config(self):
        if not self.is_container:
            return core.configs.default.Conf()
        else:
            return core.configs.docker.Conf()
