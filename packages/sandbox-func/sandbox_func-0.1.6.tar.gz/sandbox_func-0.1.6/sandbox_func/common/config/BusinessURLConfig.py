from enum import Enum

URL_DICT = {
    "DATA": "/cbn/api/v1/data",
    "METADATA": "/cbn/api/v1/metadata",
    "FLOW": "/cbn/api/v1/service",
    "SANDBOX": "/cbn/api/v1/sandbox"
}


class DataTypeEnum(Enum):
    DATA = 'DATA'
    META = 'METADATA'
    FLOW = 'FLOW'
    SANDBOX = 'SANDBOX'


class BusinessURLConfig:

    @staticmethod
    def get_url(datatype: DataTypeEnum):
        return URL_DICT[datatype.value]
