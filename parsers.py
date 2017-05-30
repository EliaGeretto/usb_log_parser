import abc


class Parser(metaclass=abc.ABCMeta):
    def __init__(self, src):
        self.__usb_data = self.retrieve_data(src)

        self.results = []
        self.__parse_entries()

    @abc.abstractmethod
    def retrieve_data(self, src):
        """Initialize the iterable object containing the data entries"""
        return None

    def __parse_entries(self):
        # TODO: Implement based on the algorithm already developed
        pass


class SyslogParser(Parser):
    def __init__(self, src):
        super().__init__(src)

    def retrieve_data(self, src):
        # TODO: Extract data from syslog file
        pass


class JournaldParser(Parser):
    def __init__(self, src):
        super().__init__(src)

    def retrieve_data(self, src):
        # TODO: Extract data from journald log
        pass
