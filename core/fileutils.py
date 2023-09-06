#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import pathlib
import os
from datetime import datetime as dt
import core.config as cfg


class FileUtils:
    def __init__(self) -> None:
        self.dt_format_to_year: str = '%Y'
        self.dt_now_year = dt.now().strftime(self.dt_format_to_year)
        self.csv_file_path: str = f'{cfg.BASE_DIR.strip("/")}/' \
                                  f'{cfg.EXPORT_DIR.strip("/")}/' \
                                  f'{cfg.CSV_FOLDER.strip("/")}/'

        self.csv_file_name: str = f'{cfg.CSV_FILENAME_PREFIX}' \
                                  f'_{cfg.CSV_FILENAME_MID}' \
                                  f'_{self.dt_now_year}' \
                                  f'.{cfg.CSV_FILE_EXTENSION}'

        # concatenate file path & file name to a single string
        self.path_csv_file: str = self.csv_file_path + self.csv_file_name

        # create the /export/csv/ folders (if they don't exist)
        self.__create_folders_export_csv()

        # create csv file for the current year (if it doesn't exist)
        self.__check_create_csv()

        # if csv file is empty -> create a CSV header
        self.__create_csv_header()

    def write_to_csv(self, data: str) -> None:
        with open(self.path_csv_file, 'a', encoding='utf8') as f:
            f.write(data + '\n')

    def __create_csv_header(self) -> None:
        file_size = os.stat(self.path_csv_file).st_size == 0
        if file_size:
            with open(self.path_csv_file, 'w', encoding='utf8') as f:
                f.write(cfg.CSV_HEADER + '\n')

    def __check_create_csv(self) -> None:
        pathlib.Path(self.path_csv_file).touch(exist_ok=True)

    @staticmethod
    def __create_folder(path: str) -> None:
        pathlib.Path(path).mkdir(exist_ok=True)

    def __create_folders_export_csv(self) -> None:
        export_dir: str = f'{cfg.BASE_DIR}/{cfg.EXPORT_DIR}'
        csv_dir: str = f'{export_dir}/{cfg.CSV_FOLDER}'
        self.__create_folder(export_dir)
        self.__create_folder(csv_dir)


if __name__ == '__main__':
    #fu = FileUtils()
    #fu.write_to_csv('test123')
    print('File:', __file__)
