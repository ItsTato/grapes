class ExtraValue(Exception):
	def __init__(self,message:str) -> None:
		super().__init__(message)
		self.__message:str = message
		return
	@property
	def message(self) -> str:
		return self.__message

class TableNotFound(Exception):
	def __init__(self,message:str) -> None:
		super().__init__(message)
		self.__message:str = message
		return
	@property
	def message(self) -> str:
		return self.__message

class EmptyRequest(Exception):
	def __init__(self, message:str) -> None:
		super().__init__(message)
		self.__message:str = message
		return
	@property
	def message(self) -> str:
		return self.__message

class TypeError(Exception):
	def __init__(self, message:str) -> None:
		super().__init__(message)
		self.__message:str = message
		return
	@property
	def message(self) -> str:
		return self.__message