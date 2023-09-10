#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import datetime as dt
import pathlib
import sys

current_ts: str = dt.datetime.now().strftime('%y-%m-%d_%H%M%S')


class Logger:
    def __init__(self, script_path: str):
        self.log_levels: dict = {
            0: 'DEBUG',
            1: 'INFO',
            2: 'WARN',
            3: 'ERROR',
            4: 'CRITICAL'
        }
        self.ts: str = current_ts
        self.file_save: bool = True
        self.file_name: str = f'log_{self.ts}.log'
        self.file_path: str = './logs'
        self.file_full_path: str = f'{self.file_path}/{self.file_name}'
        self.std: bool = True
        self.max_levels = len(self.log_levels.keys())
        self.script_path: str = script_path

        if self.file_save:
            pathlib.Path(self.file_path).mkdir(exist_ok=True)
            pathlib.Path(self.file_full_path).touch(exist_ok=True)

    def this(self, log_level: int, msg: str) -> str:
        timestamp = dt.datetime.now()
        if log_level > self.max_levels:
            err = f'{timestamp} LOGGER - ERROR: There are only {self.max_levels} log levels. You entered: {log_level}'
            print(err, file=sys.stderr)
            return err

        file_name = self._get_file_name()
        out = f'{timestamp} {self.log_levels[log_level]} [{file_name}]: {msg}'
        if self.std:
            if log_level < 3:
                print(out, file=sys.stdout)
            else:
                print(out, file=sys.stderr)
        if self.file_save:
            with open(self.file_full_path, 'a+', encoding='utf8') as f:
                f.write(self._log_out(out))
        return out

    @staticmethod
    def _log_out(log_out: str) -> str:
        return log_out + '\n'

    def _get_file_name(self) -> str:
        file_path = self.script_path.rstrip('.py')
        if '\\' in file_path:
            fp_split: list = file_path.split('\\')
        elif '/' in file_path:
            fp_split: list = file_path.split('/')
        else:
            ts = dt.datetime.now()
            err = f'{ts} LOGGER - ERROR: Unknown Error'
            print(err, file=sys.stderr)
            return err
        level1 = fp_split[-1]
        level2 = fp_split[-2]
        return f'{level2}.{level1}'
