from typing import Union

class Type:
    def __init__(self,name:str) -> None:
        self.__name:str = name.lower()
        return
    @property
    def Name(self) -> str:
        return self.__name

STRING:Type = Type("str")
INTEGER:Type = Type("int")
FLOAT:Type = Type("float")
DICTIONARY:Type = Type("dict")
BOOLEAN:Type = Type("boolean")
LIST:Type = Type("list")
TUPLE:Type = Type("tuple")

any = Union[int, str, float, bool, dict, list, tuple]
