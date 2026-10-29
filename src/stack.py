from blublib.typing import override

class Stack[T]:
    __stack__: list[T]
    def push(self, v: T) -> None: ...
    def pop(self) -> T: ...
    def top(self) -> T: ...
    def clear(self) -> None: ...




def _init():
    @override(Stack, "__init__")
    def stack_init(self: Stack):
        self.__stack__ = []

    @override(Stack, "push")
    def stack_push(self: Stack, v):
        self.__stack__.append(v)
        return
    
    @override(Stack, "pop")
    def stack_pop(self: Stack):
        return self.__stack__.pop()
    
    @override(Stack, "top")
    def stack_top(self: Stack):
        return self.__stack__[-1]
    
    @override(Stack, "clear")
    def stack_clear(self: Stack):
        self.__stack__.clear()

    @override(Stack, "__repr__", "__str__")
    def stack_stringify(self: Stack):
        return self.__stack__.__repr__()


_init()