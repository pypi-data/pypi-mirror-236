from enum import Enum


class LogLevel(Enum):
    TRACE = (1, "TRACE")
    DEBUG = (2, "DEBUG")
    INFO = (3, "INFO")
    SUCCESS = (4, "SUCCESS")
    WARNING = (5, "WARNING")
    ERROR = (6, "ERROR")
    CRITICAL = (7, "CRITICAL")

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member.fullname = name
        return member

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __str__(self):
        return self.fullname
