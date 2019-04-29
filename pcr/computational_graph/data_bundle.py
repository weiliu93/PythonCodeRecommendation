from enum import Enum
import copy


class DataBundleType(Enum):
    NORMAL = (0,)
    STOP = 1


class DataBundle(object):
    def __init__(self, data_dict=None, type=DataBundleType.NORMAL):
        assert isinstance(type, DataBundleType)
        self._data_dict = copy.copy(data_dict) if isinstance(data_dict, dict) else {}
        self._type = type

    @property
    def data_dict(self):
        return self._data_dict

    @property
    def type(self):
        return self._type

    def is_stop_signal(self):
        return self._type == DataBundleType.STOP

    def __str__(self):
        return "(data: {}, type: {})".format(self._data_dict, self._type)

    def __copy__(self):
        copy_data_dict = copy.copy(self._data_dict)
        return DataBundle(data_dict=copy_data_dict, type=self._type)

    def __getitem__(self, item):
        return self._data_dict[item]

    def __setitem__(self, key, value):
        self._data_dict[key] = value

    @staticmethod
    def stop_signal():
        return DataBundle(type=DataBundleType.STOP)
