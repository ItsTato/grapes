from .GrapesDatabase import GrapesDatabase

class CachedGrapesDatabase(GrapesDatabase):
	def __init__(self,data_directory:str="/data") -> None:
		super().__init__(data_directory=data_directory)
		self.__cache:dict = {}
		return
