from enum import IntEnum


class EDistrict(IntEnum):
    Unknown = 0
    CN = 1
    HK = 2
    TW = 4
    US = 8


class ECurrency(IntEnum):
    Unknown = 0
    AUD = 1
    CAD = 2
    CHF = 4
    CNY = 8
    EUR = 16
    GBP = 32
    JPY = 64
    NZD = 128
    USD = 256
    HKD = 512
    PLY = 1024
    CalendarCurrencyAll = 1023
