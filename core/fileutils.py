#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pathlib
import os
import sys
from datetime import datetime as dt
import core.config
import core.logger
import core.paths as paths

log = core.logger.Logger(__file__)
cfg = core.config.Interface().config()


class FileUtils:
    def __init__(self) -> None:
        self.system = sys.platform.lower()
        self.dt_format_to_year: str = '%Y'
        self.dt_now_year = dt.now().strftime(self.dt_format_to_year)
        self.csv_file_path: str = paths.CSV_FOLDER + '/'
        self.csv_file_name: str = f'{cfg.CSV_FILENAME_PREFIX}' \
                                  f'_{cfg.CSV_FILENAME_MID}' \
                                  f'_{self.dt_now_year}' \
                                  f'.{cfg.CSV_FILE_EXTENSION}'

        # concatenate file path & file name to a single string
        self.path_csv_file: str = self.csv_file_path + self.csv_file_name
        log.this(0, f'OS: {self.system}')
        log.this(0, self.path_csv_file)

        # create the /export/csv/ folders (if they don't exist)
        self.__create_folders_export_csv()

        # create csv file for the current year (if it doesn't exist)
        self.__check_create_csv()

        # if csv file is empty -> create a CSV header
        self.__create_csv_header()

    def os_path(self, path: str) -> str:
        if self.system == 'linux' or self.system == 'darwin':
            return '/' + path
        elif self.system == 'win32':
            return path
        else:
            log.this(2, 'Unknown OS, returning the standard path prefix.')
            return path

    def write_to_csv(self, data: str) -> None:
        log.this(0, 'Writing data to csv ...')
        with open(self.path_csv_file, 'a', encoding='utf8') as f:
            f.write(data + '\n')
            log.this(1, 'Wrote data to csv')

    def __create_csv_header(self) -> None:
        file_size = os.stat(self.path_csv_file).st_size == 0
        if file_size:
            log.this(0, 'Writing csv header ...')
            with open(self.path_csv_file, 'w', encoding='utf8') as f:
                f.write(cfg.CSV_HEADER + '\n')
                log.this(1, 'Wrote csv header')

    def __check_create_csv(self) -> None:
        pathlib.Path(self.path_csv_file).touch(exist_ok=True)

    @staticmethod
    def __create_folder(path: str) -> None:
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

    def __create_folders_export_csv(self) -> None:
        export_csv_dir: str = paths.CSV_FOLDER
        self.__create_folder(export_csv_dir)
