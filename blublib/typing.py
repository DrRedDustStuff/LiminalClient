from types import FunctionType, MethodType
from typing import Callable


class override:
    def __init__(self, clazz: type, *method: str) -> None:
        self.clazz = clazz
        self.method = method

    def __call__(self, fnc: Callable) -> Callable:
        for method in self.method:
            setattr(self.clazz, method, fnc)
        return fnc
