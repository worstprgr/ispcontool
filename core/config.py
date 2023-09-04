#!/usr/bin/env python 
# -*- coding:utf-8 -*-

# Absolute path recommended for BASE_DIR
BASE_DIR: str = 'M:/PYTHON/ispcontool'
EXPORT_DIR: str = 'exports'

CSV_FOLDER: str = 'csv'

# File name format will be:
#    isp_connectivity-report_2023.csv
CSV_FILENAME_PREFIX: str = 'isp'
CSV_FILENAME_MID: str = 'connectivity-report'
CSV_FILE_EXTENSION: str = 'csv'
CSV_HEADER: str = 'START,END,DURATION'


def CSV_ENTRY(dt_start: str, dt_end: str, dt_delta: str) -> str:
    return f'{dt_start},{dt_end},{dt_delta}'


HOSTS: list[str] = [
    'SH12FTgoogle.com',
    'SH12FTx.com',
    'SH12FTduckduckgo.com'
]

"""
START,END,DURATION
2023-09-01,01:15,01:30,00:15
"""

if __name__ == '__main__':
    print('')
