import abc
import re
from usb_info import UsbInfo


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
        self.__data_pattern = re.compile(
                ': New USB device found,|: USB disconnect,|: Product: |'
                ': Manufacturer: |: SerialNumber: ')

        super().__init__(src)

    def retrieve_data(self, src):
        usb_data = []
        with open(src) as origin:
            for line in origin:
                if re.search(self.__data_pattern, line):
                    usb_data.append(line)

        return usb_data


class JournaldParser(Parser):
    def __init__(self, src):
        super().__init__(src)

    def retrieve_data(self, src):
        # TODO: Extract data from journald log
        pass
