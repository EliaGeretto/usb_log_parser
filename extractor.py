from imagemounter import ImageParser
from pathlib import Path
from time import sleep
import logging

from parsers import JournaldParser, SyslogParser


class Extractor:
    def __init__(self, image_files):
        self.__image_files = image_files
        self.__results = []

    def __prepare_parser(self):
        logging.info('Parsing image from files {}'.format(self.__image_files))
        self.__image_parser = ImageParser(self.__image_files)

    def __parse_logs(self):
        for vol in self.__image_parser.init():
            vol.init_volume()
            vol_mountpoint = Path(vol.mountpoint)

            journald_log_dir = vol_mountpoint / 'var' / 'log' / 'journal'
            syslog_file = vol_mountpoint / 'var' / 'log' / 'syslog'
            if journald_log_dir.exists() and journald_log_dir.is_dir():
                logging.info('Found systemd journal log in volume {}'.format(
                        vol.index))
                info_parser = JournaldParser(str(journald_log_dir.resolve()))
                self.__results += info_parser.results
            elif syslog_file.exists() and syslog_file.is_file():
                logging.info('Found syslog log in volume {}'.format(
                        vol.index))
                info_parser = SyslogParser(str(syslog_file.resolve()))
                self.__results += info_parser.results

    def __unmount_volumes(self):
        self.__image_parser.clean()

    def get_usb_info(self):
        self.__prepare_parser()
        self.__parse_logs()

        # Otherwise it is too fast
        sleep(0.1)
        self.__unmount_volumes()

        if self.__results == []:
            logging.error('No log was found in any volume')

        return self.__results
