from .__meta__ import GRAPES_VERSION, PYTHON_VERSION
from .Column import Column

class Table:
	def __init__(self,table_name:str,columns:list[Column]) -> None:
		self.__GRAPES_VERSION:str = GRAPES_VERSION
		self.__PYTHON_VERSION:str = PYTHON_VERSION
		self.__table_name:str = table_name
		self.__columns:list[Column] = columns
		self.__last:int = 0

	@property
	def GRAPES_VERSION(self) -> str:
		return self.__GRAPES_VERSION
	@property
	def PYTHON_VERSION(self) -> str:
		return self.__PYTHON_VERSION
	@property
	def Name(self) -> str:
		return self.__table_name
	@property
	def Columns(self) -> list[Column]:
		return self.__columns
	@property
	def Last(self) -> int:
		return self.__last
	@Last.setter
	def Last(self,new_value:int) -> None:
		self.__last = new_value
