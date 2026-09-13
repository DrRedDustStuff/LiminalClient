

class UnhandledCase(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("This path of execution has not been handled yet",*args)
