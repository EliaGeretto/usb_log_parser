import abc


class Parser(metaclass=abc.ABCMeta):
    def __init__(self, src):
        self.__usb_data = self.retrieve_data(src)

        self.__results = []
        self.__parse_entries()

    @abc.abstractmethod
    def retrieve_data(self, src):
        """Initialize the iterable object containing the data entries"""
        return None

    def __iter__(self):
        return iter(self.__results)

    def __parse_entries():
        # TODO: Implement based on the algorithm already developed
        pass


class SyslogParser(Parser):
    pass


class JournaldParser(Parser):
    pass
