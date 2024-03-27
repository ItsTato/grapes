from typing import Union

from .Types import Type, any
from .Errors.ColumnError import ColumnInvalidSetting

class Column:
	def __init__(self,name:str,type:Type,default_value:any="",auto_increment:bool=False,increment_by:Union[int,float]=1) -> None:
		self.__name:str = name
		self.__type:Type = type
		self.__default_value:any = default_value
		self.__auto_increment:bool = auto_increment
		self.__increment_by:Union[int,float] = increment_by
		if (type.Name != "integer" and type.Name != "float") and auto_increment:
			raise ColumnInvalidSetting("You cannot use auto increments on anything other than integers or floats.")
		return
	@property
	def Name(self) -> str:
		return self.__name
	@property
	def OfType(self) -> Type:
		return self.__type
	@property
	def DefaultValue(self) -> any:
		return self.__default_value
	@property
	def AutoIncrement(self) -> bool:
		return self.__auto_increment
	@property
	def IncrementBy(self) -> Union[int,float]:
		return self.__increment_by