import os, pickle

from .Table import Table
from .Errors import TableError, InsertError, GetError
from .Types import any

# Tato's Notes-To-Self #

# Use shutil for backup operations
# (it can handle big copies of folders easily)
# (same with compression)

class GrapesDatabase:
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
		self.__update_definition()
		return
	
	def __generate_files(self,dir_structure:dict) -> None:
		for parent, children in dir_structure.items():
			if not os.path.exists(parent):
				os.mkdir(parent)
			if isinstance(children,dict):
				self.__generate_files(children)
			elif not os.path.exists(children):
				os.mkdir(children)
		return
	
	def __update_definition(self) -> None:
		with open(f"{self.__tables_dir}/definition.bin","rb") as file:
			self.__tables = pickle.load(file)
			file.close()
		return
	
	def __upgrade_definition(self) -> None:
		with open(f"{self.__tables_dir}/definition.bin","wb") as file:
			pickle.dump(self.__tables,file)
			file.close()
		return
	
	def force_reload(self) -> None:
		self.__generate_files(self.__dir_structure)
		self.__update_definition()
	
	def create_table(self,table:Table) -> None:
		if table.Name in self.__tables:
			raise TableError.TableAlreadyExists(f"A table with the name \"{table.Name}\" already exists!")
		if table.Name.replace(" ","") == "":
			raise TableError.TableNameIsBlankOrInvalid(f"Table name cannot be blank!")
		special_characters:list = ["<",">",":","\"","/","\\","|","?","*"] # god i hate binbows and copiumOS
		for special_char in special_characters:
			if table.Name.find(special_char) != False:
				raise TableError.TableNameIsBlankOrInvalid(f"You cannot use special characters in the table name! ({special_char})")
		if len(table.Columns) == 0:
			raise TableError.TableHasNoColumns(f"Tables must have at least one (1) table.")
		with open(f"{self.__tables_dir}/definition.bin","r+b") as file:
			definition:dict = pickle.load(file)
			definition[table.Name] = table
			pickle.dump(definition,file)
			file.close()
		self.__tables[table.Name] = table
		with open(f"{self.__tables_dir}/{table.Name}.grape","wb") as file:
			pickle.dump([],file)
			file.close()
		return
	
	def delete_table(self,table_name:str) -> None:
		if table_name not in self.__tables:
			raise TableError.TableDoesNotExist(f"No table with the name \"{table_name}\" exists.")
		os.remove(f"{self.__tables_dir}/{table_name}.grape")
		del self.__tables[table_name]
		with open(f"{self.__tables_dir}/definition.bin","wb") as file:
			pickle.dump(self.__tables,file)
			file.close()
	
	def has_table(self,table_name:str) -> bool:
		return table_name in self.__tables
	
	def insert_into(self,table_name:str,values:tuple[any]) -> None:
		if table_name not in self.__tables:
			raise InsertError.TableNotFound(f"No table with the name {table_name} could be found.")
		if len(values) == 0:
			raise InsertError.EmptyRequest("At least one (1) value must be provided in the request.")
		if len(values) > self.__tables[table_name].Columns:
			raise InsertError.ExtraValue("The request has more values than the table has columns.")
		self.__tables[table_name].Last += 1
		self.__upgrade_definition()
		with open(f"{self.__tables_dir}/{table_name}.grape","rb") as file:
			data:list[tuple] = pickle.load(file)
			file.close()
		if len(values) < len(self.__tables[table_name].Columns):
			for index, column in enumerate(self.__tables[table_name].Columns):
				if len(values) < index:
					values += (column.Default,) # type: ignore
		data.append(values)
		with open(f"{self.__tables_dir}/{table_name}.grape","wb") as file:
			pickle.dump(data,file)
			file.close()
		