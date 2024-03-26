import os, json

# Tato's Notes-To-Self #

# Use shutil for backup operations
# (it can handle big copies of folders easily)
# (same with compression)

class CachedDatabase:
	def __init__(self,data_directory:str="/data") -> None:
		self.__main_dir:str = os.path.dirname(os.path.realpath(__file__))
		self.__data_dir:str = f"{self.__main_dir}{data_directory}"
		self.__table_dir:str = f"{self.__data_dir}/tables"

		self.__dir_structure = {
			self.__data_dir: {
				self.__table_dir: {}
			}
		}
		
		def generate_files(dir_structure:dict):
			for parent, children in dir_structure.items():
				if not os.path.exists(parent):
					os.mkdir(parent)

				if isinstance(children, dict):					
					generate_files(children)
				elif not os.path.exists(children):
					os.mkdir(children)
		
		generate_files(self.__dir_structure)

		self.__cache:dict = {}

		return
