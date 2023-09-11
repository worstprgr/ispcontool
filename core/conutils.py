#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import sys


def is_container():
    current_platform: str = sys.platform.lower()

    if current_platform in ['linux', 'darwin']:
        with open('/proc/self/cgroup', 'r') as p:
            for x in p:
                fields = x.strip().split('/')
                if fields[1] == 'docker':
                    return True
    elif current_platform in ['win32']:
        # not implemented yet
        # wth do you would even run a container in a Windows env?!
        return False
    else:
        return False
