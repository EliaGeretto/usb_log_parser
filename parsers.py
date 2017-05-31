from systemd import journal
from collections import namedtuple
from datetime import datetime
import abc
import re

from usb_info import UsbInfo


LogEntry = namedtuple('LogEntry', ['timestamp', 'message'])


# XXX: Needs review, given the new internal API
class Parser(metaclass=abc.ABCMeta):
    def __init__(self, src):
        self.__usb_data = self.retrieve_data(src)

        self.__new_usb_pattern = re.compile(': New USB device found,')
        self.__dis_usb_pattern = re.compile(': USB disconnect,')
        self.__product_pattern = re.compile(': Product: ')
        self.__manufac_pattern = re.compile(': Manufacturer: ')
        self.__serial_pattern = re.compile(': SerialNumber: ')

        self.results = []
        self.__parse_entries()

    @abc.abstractmethod
    def retrieve_data(self, src):
        """Initialize the iterable object containing the data entries"""
        return None

    def __parse_entries(self):
        dictio = {}
        for line in self.__usb_data:
            if re.search(self.__new_usb_pattern, line):
                name = re.split(':', re.split('usb ', line)[1])[0]
                temp = UsbInfo()
                temp.time_in = line[:15]
                if name in dictio:
                    self.results.append(dictio[name])
                dictio[name] = temp
            elif re.search(self.__product_pattern, line):
                name = re.split(':', re.split('usb ', line)[1])[0]
                prod = re.split(self.__product_pattern, line)[1]
                dictio[name].product = prod.rstrip()
            elif re.search(self.__manufac_pattern, line):
                name = re.split(':', re.split('usb ', line)[1])[0]
                manu = re.split(self.__manufac_pattern, line)[1]
                dictio[name].manufact = manu.rstrip()
            elif re.search(self.__serial_pattern, line):
                name = re.split(':', re.split('usb ', line)[1])[0]
                seria = re.split(self.__serial_pattern, line)[1]
                dictio[name].serial = seria.rstrip()
            elif re.search(self.__dis_usb_pattern, line):
                name = re.split(':', re.split('usb ', line)[1])[0]
                dictio[name].time_out = line[:15]

        for res in dictio.values():
            self.results.append(res)


class SyslogParser(Parser):
    def __init__(self, src):
        # The method retrieve_data will be called by the constructor of the
        # parent class, thus this initialization goes before the call to it.
        self.__kern_pattern = re.compile('kernel: \[\s*[0-9]+\.[0-9]+\] ')

        super().__init__(src)

    def retrieve_data(self, src):
        usb_entries = []
        with open(src) as syslog:
            for line in syslog:
                # Kernel log message
                if re.search(self.__kern_pattern, line):
                    message = re.split(self.__kern_pattern, line)[1]
                    # USB subsystem message
                    if message.startswith('usb') or message.startswith('hub'):
                        date_string = line[:15]
                        date = datetime.strptime(
                                date_string, '%b %d %H:%M:%S')
                        log_entry = LogEntry(date, message)
                        usb_entries.append(log_entry)

        return usb_entries


class JournaldParser(Parser):
    def __init__(self, src):
        super().__init__(src)

    def retrieve_data(self, src):
        reader = journal.Reader(path=src)
        reader.add_match(_KERNEL_SUBSYSTEM='usb')

        usb_entries = []
        for journal_entry in reader:
            # The __REALTIME_TIMESTAMP is already a datetime object
            log_entry = LogEntry(
                    journal_entry['__REALTIME_TIMESTAMP'],
                    journal_entry['MESSAGE'])
            usb_entries.append(log_entry)
        reader.close()

        return usb_entries
