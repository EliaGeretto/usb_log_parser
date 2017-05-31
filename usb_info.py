import unittest
from datetime import datetime


class UsbInfo:

    DATETIME_FMT = '%b %d %H:%M:%S'
    UNKNOWN_STR = 'Unknown'

    def __init__(self):
        self.product = None
        self.manufact = None
        self.serial = None
        self.__time_in = None
        self.__time_out = None

    @property
    def time_in(self):
        return self.__time_in.strftime(UsbInfo.DATETIME_FMT) \
                if self.__time_in is not None else None

    @time_in.setter
    def time_in(self, value):
        self.__time_in = value

    @property
    def time_out(self):
        return self.__time_out.strftime(UsbInfo.DATETIME_FMT) \
                if self.__time_out is not None else None

    @time_out.setter
    def time_out(self, value):
        self.__time_out = value

    def __str__(self):
        return ('| {:20} | {:20} | {:20} | {:20} | {:20} |'.format(
                self.product[:20] if self.product is not None
                        else UsbInfo.UNKNOWN_STR,
                self.manufact[:20] if self.manufact is not None
                        else UsbInfo.UNKNOWN_STR,
                self.serial[:20] if self.serial is not None
                        else UsbInfo.UNKNOWN_STR,
                self.time_in[:20] if self.time_in is not None
                        else UsbInfo.UNKNOWN_STR,
                self.time_out[:20] if self.time_out is not None
                        else UsbInfo.UNKNOWN_STR))
