from imagemounter import ImageParser
from pathlib import Path
from time import sleep

from parsers import JournaldParser, SyslogParser


class Extractor:
    def __init__(self, image_files):
        self.__image_files = image_files

    def __mount_volume(self):
        print('Parsing image from file:', self.__image_files)
        self.__image_parser = ImageParser(self.__image_files)

        for vol in self.__image_parser.init():
            if vol.size > 1024 * 1024:
                print('Found suitable volume:', vol)
                self.__volume = vol
                break

        print('Mounting volume.')
        self.__volume.init_volume()

    def __unmount_volume(self):
        print('Unmounting volume.')
        self.__image_parser.clean()

    def __init_log_parser(self):
        vol_mountpoint = Path(self.__volume.mountpoint)

        journald_log_dir = vol_mountpoint / 'var' / 'log' / 'journal'
        syslog_file = vol_mountpoint / 'var' / 'log' / 'syslog'
        if journald_log_dir.exists() and journald_log_dir.is_dir():
            print('Found journald log.')
            self.__info_parser = JournaldParser(
                    str(journald_log_dir.resolve()))
        elif syslog_file.exists() and syslog_file.is_file():
            print('Found syslog log.')
            self.__info_parser = SyslogParser(
                    str(syslog_file.resolve()))
        else:
            print('No matching log found.')

    def get_usb_info(self):
        self.__mount_volume()
        self.__init_log_parser()

        # Otherwise it is too fast
        sleep(0.5)
        self.__unmount_volume()

        return self.__info_parser.results
