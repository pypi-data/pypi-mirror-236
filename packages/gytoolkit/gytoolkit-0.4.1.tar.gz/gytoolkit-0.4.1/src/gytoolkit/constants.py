"""
common constant definition used in gytoolkit
"""
from dataclasses import dataclass
from datetime import datetime

class SingletonMeta(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        key = tuple(kwargs.get(attr) for attr in cls.__singleton_attributes__)
        if key not in cls.instances:
            cls.instances[key] = super().__call__(*args, **kwargs)
        else:
            # 更新属性
            instance = cls.instances[key]
            for attr, value in kwargs.items():
                if attr not in cls.__singleton_attributes__:
                    setattr(instance, attr, value)
        return cls.instances[key]

@dataclass
class NetValueData(metaclass=SingletonMeta):
    __singleton_attributes__ = ('date', 'prodcode')
    date:datetime
    prodcode:str
    netvalue:float
    cum_netvalue:float
    prodname:str = None
    netasset:float = None
    shares:float = None