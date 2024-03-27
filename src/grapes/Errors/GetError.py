class TableNotFound(Exception):
	def __init__(self, message:str) -> None:
		self.__message:str = message
	@property
	def message(self) -> str:
		return self.__message