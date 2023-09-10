#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import core.cfg_default
import core.cfg_docker

docker_conf: bool = True


class Interface:
    def __init__(self):
        if not docker_conf:
            self.config = core.cfg_default.Conf()
        else:
            self.config = core.cfg_docker.Conf()
