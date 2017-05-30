import unittest
from datetime import datetime


DATETIME_FMT_IN = '%b %d %H:%M:%S'
DATETIME_FMT_OUT = '%B %d %H:%M:%S'


class UsbInfo:
    def __init__(self):
        self.product = None
        self.manufact = None
        self.serial = None
        self.__time_in = None
        self.__time_out = None

    @property
    def time_in(self):
        return self.__time_in.strftime(DATETIME_FMT_OUT) \
                if self.__time_in is not None else None

    @time_in.setter
    def time_in(self, value):
        self.__time_in = datetime.strptime(value, DATETIME_FMT_IN)

    @property
    def time_out(self):
        return self.__time_out.strftime(DATETIME_FMT_OUT) \
                if self.__time_out is not None else None

    @time_out.setter
    def time_out(self, value):
        self.__time_out = datetime.strptime(value, DATETIME_FMT_IN)

    def __str__(self):
        return ('Product: {} ; Manufacturer: {} ; Serial number: {} ; '
                'Insertion: {} ; Expulsion: {}'.format(
                        self.product, self.manufact, self.serial,
                        self.time_in, self.time_out))


class UsbInfoTest(unittest.TestCase):
    def setUp(self):
        self.usb_info = UsbInfo()

    def test_empty_object(self):
        self.assertEqual(str(self.usb_info),
                         ('Product: None ; Manufacturer: None ; '
                          'Serial number: None ; Insertion: None ; '
                          'Expulsion: None'))

    def test_full_object(self):
        self.usb_info.product = 'Hello'
        self.usb_info.manufact = 'World'
        self.usb_info.serial = '123456'
        self.usb_info.time_in = 'May  5 05:05:05'
        self.usb_info.time_out = 'Oct 10 10:10:10'

        self.assertEqual(str(self.usb_info),
                         ('Product: Hello ; Manufacturer: World ; '
                          'Serial number: 123456 ; '
                          'Insertion: May 05 05:05:05 ; '
                          'Expulsion: October 10 10:10:10'))


if __name__ == '__main__':
    unittest.main()
