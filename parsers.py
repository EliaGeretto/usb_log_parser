from systemd import journal
from collections import namedtuple
from datetime import datetime
import abc
import re
import logging

from usb_info import UsbInfo


LogEntry = namedtuple('LogEntry', ['timestamp', 'message'])


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
        logging.info('Parsing USB subsystem messages')

        dictio = {}
        for log_entry in self.__usb_data:
            if re.search(self.__new_usb_pattern, log_entry.message):
                name = log_entry.message.split(':')[0]
                idVendor = log_entry.message.split(',')[1].strip()
                idProduct = log_entry.message.split(',')[2].strip()
                temp = UsbInfo()
                temp.product = idProduct
                temp.manufact = idVendor
                temp.time_in = log_entry.timestamp
                if name in dictio:
                    self.results.append(dictio[name])
                    logging.debug('({}) entry elimination'.format(name))
                dictio[name] = temp
                logging.debug('({}) new device'.format(name))

            elif re.search(self.__product_pattern, log_entry.message):
                name = log_entry.message.split(':')[0]
                prod = re.split(self.__product_pattern, log_entry.message)[1]
                dictio[name].product = prod.rstrip()
                logging.debug('({}) product "{}"'.format(
                        name, dictio[name].product))

            elif re.search(self.__manufac_pattern, log_entry.message):
                name = log_entry.message.split(':')[0]
                manu = re.split(self.__manufac_pattern, log_entry.message)[1]
                dictio[name].manufact = manu.rstrip()
                logging.debug('({}) manufacturer "{}"'.format(
                        name, dictio[name].manufact))

            elif re.search(self.__serial_pattern, log_entry.message):
                name = log_entry.message.split(':')[0]
                seria = re.split(self.__serial_pattern, log_entry.message)[1]
                dictio[name].serial = seria.rstrip()
                logging.debug('({}) serial "{}"'.format(
                        name, dictio[name].serial))

            elif re.search(self.__dis_usb_pattern, log_entry.message):
                name = log_entry.message.split(':')[0]
                dictio[name].time_out = log_entry.timestamp
                logging.debug('({}) disconnect "{}"'.format(
                        name, dictio[name].time_out))

        for res in dictio.values():
            self.results.append(res)

        self.results.sort(key=lambda entry: entry.time_in)


class SyslogParser(Parser):
    def __init__(self, src):
        # The method retrieve_data will be called by the constructor of the
        # parent class, thus this initialization goes before the call to it.
        self.__kern_pattern = re.compile('kernel: \[\s*[0-9]+\.[0-9]+\] ')

        super().__init__(src)

    def retrieve_data(self, src):
        logging.info('Retrieving data from syslog file')
        usb_entries = []
        with open(src) as syslog:
            for line in syslog:
                # Kernel log message
                if re.search(self.__kern_pattern, line):
                    message = re.split(self.__kern_pattern, line)[1].strip()
                    # USB subsystem message
                    if message.startswith('usb') or message.startswith('hub'):
                        date_string = line[:15]
                        date = datetime.strptime(
                                date_string, '%b %d %H:%M:%S')
                        log_entry = LogEntry(date, message)
                        usb_entries.append(log_entry)
                        logging.debug('Extracted line "{}"\t"{}"'.format(
                                log_entry.timestamp, log_entry.message))

        return usb_entries


class JournaldParser(Parser):
    def __init__(self, src):
        super().__init__(src)

    def retrieve_data(self, src):
        logging.info('Retrieving data from systemd journal directory')
        reader = journal.Reader(path=src)
        reader.add_match(_KERNEL_SUBSYSTEM='usb')

        usb_entries = []
        for journal_entry in reader:
            # The __REALTIME_TIMESTAMP is already a datetime object
            log_entry = LogEntry(
                    journal_entry['__REALTIME_TIMESTAMP'],
                    journal_entry['MESSAGE'])
            usb_entries.append(log_entry)
            logging.debug('Extracted line "{}"\t"{}"'.format(
                    log_entry.timestamp, log_entry.message))
        reader.close()

        return usb_entries
