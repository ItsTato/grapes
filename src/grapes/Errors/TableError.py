class TableAlreadyExists(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)
        self.__message:str = message
    @property
    def message(self) -> str:
        return self.__message

class TableNameIsBlankOrInvalid(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)
        self.__message:str = message
    @property
    def message(self) -> str:
        return self.__message

class TableHasNoColumns(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)
        self.__message:str = message
    @property
    def message(self) -> str:
        return self.__message

class TableDoesNotExist(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)
        self.__message:str = message
    @property
    def message(self) -> str:
        return self.__message