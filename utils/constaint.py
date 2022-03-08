"""

"""
from enum import Enum
from types import DynamicClassAttribute


# 为Pydantic定义枚举值类
class EBase(Enum):
    @classmethod
    def __init__(cls):
        cls.values = {}

    def __repr__(self):
        return f'"{self._value_}"'

    def __str__(self):
        return f'"{self._value_}"'

    @DynamicClassAttribute
    def cname(self):
        """ 返回中文名称"""
        return self.values.get(self.value)

    @classmethod
    def fmt(cls):
        """
        将枚举值及代表含义格式化
        :return:
        :rtype:
        """
        ret = []
        for m in cls._value2member_map_.keys():
            ret.append(f'{m}:{cls.values.get(m)}')
        return ','.join(ret)


class EExampleType(str, EBase):
    """
    枚举类型例子
    """

    @classmethod
    def __init__(cls, *args):
        super().__init__()
        cls.values = {
            0: '例子0',
            1: '例子1',
        }

    example0 = 0
    example1 = 1
