import os, json

from .Errors import TableError

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
				if column != "def.json":
					self.__tables[table][column] = {}
					# Get a definition from the table's
					# index.json file of the order of
					# tables.
		return
	
	def force_reload(self) -> None:
		self.__generate_files(self.__dir_structure)
		self.__get_tables(self.__tables_dir)

	def create_table(self,table_name:str,columns:list=[]) -> None:
		if table_name in self.__tables:
			raise TableError.TableAlreadyExists(f"There's already a table called {table_name} in the database.")
		if table_name.replace(" ", "") == "":
			raise TableError.TableNameIsBlankOrInvalid(f"Table name cannot be blank.")
		special_characters:list = ["\\","/",";","*","?","\"","<",">","|"] # got i hate windows and macos
		for special_char in special_characters:
			if table_name.find(special_char) != -1:
				raise TableError.TableNameIsBlankOrInvalid(f"The table name cannot have any special characters in it.")
		
		os.mkdir(f"{self.__tables_dir}/{table_name}")
		index:dict = {
			"last": 0
		}
		if len(columns) == 0:
			raise TableError.TableHasNoColumns("Tables must have at least one (1) column when first created.")
		for column in columns:
			index[f"{column.Name}"] = {
				"type": column.OfType.Name,
				"default": column.DefaultValue,
				"auto_increment": column.AutoIncrement,
				"increment_by": column.IncrementBy
			}
			with open(f"{self.__tables_dir}/{table_name}/{column.Name}.grapelet","wb") as file:
				file.write(b"")
				file.close()

		with open(f"{self.__tables_dir}/{table_name}/def.json","w") as file:
			json.dump(index,file)
			file.close()
		
		return
