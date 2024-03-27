import os, shutil, pickle

from .Errors import TableError, InsertError

# Tato's Notes-To-Self #

# Use shutil for backup operations
# (it can handle big copies of folders easily)
# (same with compression)

class Database:
	def __init__(self,data_directory:str="/data") -> None:
		self.__main_dir:str = os.path.dirname(os.path.realpath(__file__))
		self.__data_dir:str = f"{self.__main_dir}{data_directory}"
		self.__tables_dir:str = f"{self.__data_dir}/tables"
		self.__dir_structure:dict = {
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
			with open(f"{tables_dir}/{table}/def.bin","rb") as file:
				definition:dict = pickle.load(file)
				file.close()
			self.__tables[table] = definition
		return
	
	def force_reload(self) -> None:
		self.__generate_files(self.__dir_structure)
		self.__get_tables(self.__tables_dir)

	def create_table(self,table_name:str,columns:list=[]) -> None:
		if table_name in self.__tables:
			raise TableError.TableAlreadyExists(f"There's already a table called {table_name} in the database.")
		if table_name.replace(" ", "") == "":
			raise TableError.TableNameIsBlankOrInvalid(f"Table name cannot be blank.")
		special_characters:list = ["\\","/",";","*","?","\"","<",">","|"] # god i hate binbows and copiumOS
		for special_char in special_characters:
			if table_name.find(special_char) != -1:
				raise TableError.TableNameIsBlankOrInvalid(f"The table name cannot have any special characters in it.")
		os.mkdir(f"{self.__tables_dir}/{table_name}")
		definition:dict = {
			"last": 0,
			"columns": {}
		}
		if len(columns) == 0:
			raise TableError.TableHasNoColumns("Tables must have at least one (1) column when first created.")
		for column in columns:
			definition["columns"][f"{column.Name}"] = column
			with open(f"{self.__tables_dir}/{table_name}/{column.Name}.grapelet","wb") as file:
				pickle.dump([],file)
				file.close()
		with open(f"{self.__tables_dir}/{table_name}/def.bin","wb") as file:
			pickle.dump(definition,file)
			file.close()
		self.__get_tables(self.__tables_dir)
		return
	
	def delete_table(self,table_name:str) -> None:
		if table_name not in self.__tables:
			raise TableError.TableDoesNotExist(f"No table with the name {table_name} was found in the database.")
		shutil.rmtree(f"{self.__tables_dir}/{table_name}",False)
		del self.__tables[table_name]
		return
	
	def has_table(self,table_name:str) -> bool:
		return table_name in self.__tables
	
	def insert_into(self,table_name:str,values:tuple) -> None:
		if table_name not in self.__tables:
			raise InsertError.TableNotFound(f"Table {table_name} does not exist.")
		if len(values) == 0:
			raise InsertError.EmptyRequest("Please provide at least one (1) value in the request.")
		if len(values) > self.__tables[table_name]:
			raise InsertError.ExtraValue("An extra value was / Extra values were provided in the request")
		self.__tables["last"] += 1
		columns_iterable:list = list(self.__tables["columns"].items())
		for index, value in enumerate(values):
			with open(f"{self.__tables_dir}/{table_name}/{columns_iterable[index]}","r+b") as file:
				data = pickle.load(file)
				data.append(value)
				pickle.dump(data,file)
				file.close()
		return
