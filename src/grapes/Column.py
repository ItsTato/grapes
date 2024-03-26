from .Types import Type
	
class Column:
	def __init__(self,name:str,type:Type) -> None:
		self.__name:str = name
		self.__type:Type = type
		return
	@property
	def Name(self) -> str:
		return self.__name
	@property
	def Of(self) -> Type:
		return self.__type