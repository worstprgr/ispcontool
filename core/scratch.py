#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import core.config

cfg = core.config.Interface().config

if __name__ == '__main__':
    print(cfg.EXPORT_DIR)
