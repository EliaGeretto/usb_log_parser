import abc
import re
from usb_info import UsbInfo


class Parser(metaclass=abc.ABCMeta):
    def __init__(self, src):
        self.__usb_data = self.retrieve_data(src)

        self.results = []
        self.__parse_entries()

        self.new_usb_pattern = re.compile(': New USB device found,')
        self.dis_usb_pattern = re.compile(': USB disconnect,')
        self.product_pattern = re.compile(': Product: ')
        self.manufac_pattern = re.compile(': Manufacturer: ')
        self.serial_pattern = re.compile(': SerialNumber: ')

    @abc.abstractmethod
    def retrieve_data(self, src):
        """Initialize the iterable object containing the data entries"""
        return None

    def __parse_entries(self):
        dictio = {}
        for line in self.__usb_data:
            if re.search(self.new_usb_pattern, line):
                name = re.split(':',re.split('usb ', line)[1])[0]
                temp = UsbInfo()
                temp.time_in(line[:15])
                if name in dictio:
                    self.result.append(dictio[name])
                dictio[name] = temp
            elif re.search(self.product_pattern, line):
                name = re.split(':',re.split('usb ', line)[1])[0]
                prod = re.split(self.product_pattern, line)[1]
                dictio[name].product = prod.rstrip()
            elif re.search(self.manufac_pattern, line):
                name = re.split(':',re.split('usb ', line)[1])[0]
                manu = re.split(self.manufac_pattern, line)[1]
                dictio[name].manufact = manu.rstrip()
            elif re.search(self.serial_pattern, line):
                name = re.split(':',re.split('usb ', line)[1])[0]
                seria = re.split(self.serial_pattern, line)[1]
                dictio[name].serial = seria.rstrip()
            elif re.search(self.dis_usb_pattern, line):
                name = re.split(':',re.split('usb ', line)[1])[0]
                dictio[name].time_out(line[:15])
            else:
                continue
        for key in dictio:
            self.result.append(dictio[key])


class SyslogParser(Parser):
    def __init__(self, src):
        super().__init__(src)
        self.__data_pattern = re.compile(
                ': New USB device found,|: USB disconnect,|: Product: |'
                ': Manufacturer: |: SerialNumber: ')

    def retrieve_data(self, src):
        usb_data = []
        self.__data_pattern = re.compile(
                ': New USB device found,|: USB disconnect,|: Product: |'
                ': Manufacturer: |: SerialNumber: ')
        with open(src) as origin:
            for line in origin:
                if re.search(self.__data_pattern, line):
                    usb_data.append(line)
                else:
                    continue


class JournaldParser(Parser):
    def __init__(self, src):
        super().__init__(src)

    def retrieve_data(self, src):
        # TODO: Extract data from journald log
        pass
