#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import os
import re
import datetime


def set_base_path() -> str:
    # minilog
    def log(msg):
        dt = datetime.datetime.now()
        out = f'{dt} INFO [setup]: {msg}'
        print(out)
        return out

    paths_py: str = 'core/paths.py'
    current_dir: str = os.path.abspath('')
    current_dir = current_dir.replace('\\', '/')
    log(f'Current Dir: {current_dir}')

    log(f'Reading {paths_py} ...')
    with open(paths_py, 'r', encoding='utf8') as f:
        pyfile = f.read()
    log('Reading done')

    log('Replacing strings ...')
    pattern = r"BASE_DIR: str = r'.+'"
    replace_by = f"BASE_DIR: str = r'{current_dir}'"
    pyfile = re.sub(pattern, replace_by, pyfile)
    log('Strings replaced')

    log(f'Writing content into {paths_py} ...')
    with open(paths_py, 'w+', encoding='utf8') as p:
        p.write(pyfile)
    log('Done writing')


if __name__ == '__main__':
    set_base_path()
