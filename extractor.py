from imagemounter import ImageParser
from pathlib import Path
from time import sleep
import logging

from parsers import JournaldParser, SyslogParser


class Extractor:
    def __init__(self, image_files):
        self.__image_files = image_files

    def __mount_volume(self):
        logging.info('Parsing image from files {}'.format(self.__image_files))
        self.__image_parser = ImageParser(self.__image_files)

        for vol in self.__image_parser.init():
            if vol.size > 1024 * 1024:
                logging.info('Found suitable volume {}'.format(vol.index))
                self.__volume = vol
                break

        self.__volume.init_volume()

    def __unmount_volume(self):
        self.__image_parser.clean()

    def __init_log_parser(self):
        vol_mountpoint = Path(self.__volume.mountpoint)

        journald_log_dir = vol_mountpoint / 'var' / 'log' / 'journal'
        syslog_file = vol_mountpoint / 'var' / 'log' / 'syslog'
        if journald_log_dir.exists() and journald_log_dir.is_dir():
            logging.info('Found systemd journal log in volume {}'.format(
                    self.__volume.index))
            self.__info_parser = JournaldParser(
                    str(journald_log_dir.resolve()))
        elif syslog_file.exists() and syslog_file.is_file():
            logging.info('Found syslog log in volume {}'.format(
                    self.__volume.index))
            self.__info_parser = SyslogParser(
                    str(syslog_file.resolve()))
        else:
            logging.error('No log found')

    def get_usb_info(self):
        self.__mount_volume()
        self.__init_log_parser()

        # Otherwise it is too fast
        sleep(0.1)
        self.__unmount_volume()

        return self.__info_parser.results
