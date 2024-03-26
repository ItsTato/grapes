import os
from .Database import Database

# Tato's Notes-To-Self #

# Use shutil for backup operations
# (it can handle big copies of folders easily)
# (same with compression)

class CachedDatabase(Database):
	def __init__(self,data_directory:str="/data") -> None:
		super().__init__(data_directory=data_directory)
		self.__cache:dict = {}
		return
