import os

# Tato's Notes-To-Self #

# Use shutil for backup operations
# (it can handle big copies of folders easily)
# (same with compression)

class Database:
	def __init__(self,data_directory:str="/data") -> None:
		self.__main_dir:str = os.path.dirname(os.path.realpath(__file__))
		self.__data_dir:str = f"{self.__main_dir}{data_directory}"
		self.__tables_dir:str = f"{self.__data_dir}/tables"
		self.__dir_structure = {
			self.__data_dir: {
				self.__tables_dir: {}
			}
		}
		self.__tables:dict = {}
		
		self.__generate_files(self.__dir_structure)
		self.__get_tables(self.__tables_dir)

		print(self.__tables)

		return
	
	def __generate_files(self,dir_structure:dict) -> None:
		for parent, children in dir_structure.items():
			if not os.path.exists(parent):
				os.mkdir(parent)
			if isinstance(children, dict):					
				self.__generate_files(children)
			elif not os.path.exists(children):
				os.mkdir(children)
		return
	
	def __get_tables(self,tables_dir:str) -> None:
		for table in os.listdir(tables_dir):
			self.__tables[table] = {}
			for column in os.listdir(os.path.join(tables_dir, table)):
				if column != "index.json":
					self.__tables[table][column] = {}
					# Get a definition from the table's
					# index.json file of the order of
					# tables.
		return
