class ColumnInvalidSetting(Exception):
    def __init__(self, message:str) -> None:
        super().__init__(message)
        self.__message:str = message
    @property
    def message(self) -> str:
        return self.__message