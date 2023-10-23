from abc import ABCMeta
from inspect import signature


class EventListener(metaclass=ABCMeta):
    @classmethod
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return (
            hasattr(__subclass, "notify")
            and callable(__subclass.notify)
            and {"self", "event", "args", "kwargs"}.issubset(
                set(signature(__subclass.notify).parameters.keys())
            )
        )
