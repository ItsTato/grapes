import os, pickle
from typing import Union, Any

from .Table import Table
from .Errors import TableError, InsertError, GetError
from .__meta__ import GRAPES_VERSION, PYTHON_VERSION

# Tato's Notes-To-Self #

# Use shutil for backup operations
# (it can handle big copies of folders easily)
# (same with compression)

class GrapesDatabase:
	def __init__(self,file_loc:str,data_directory:str="./data",force_through_warnings:bool=False) -> None:
		self.__force_through_warnings:bool = force_through_warnings
		self.__main_dir:str = os.path.dirname(os.path.realpath(file_loc)) if "." in data_directory else os.path.dirname(os.path.realpath(data_directory))
		self.__data_dir:str = os.path.join(self.__main_dir,data_directory)
		self.__tables_dir:str = f"{self.__data_dir}/tables"
		self.__dir_structure:dict = {
			self.__data_dir: {
				self.__tables_dir: {}
			}
		}
		self.__tables:dict = {}
		self.__generate_files(self.__dir_structure)
		if os.path.exists(f"{self.__tables_dir}/definition.bin"):
			self.__update_definition()
		else:
			self.__upgrade_definition()
		warn_grapes:bool = False
		warn_python:bool = False
		for table in self.__tables:
			if self.__tables[table].GRAPES_VERSION != GRAPES_VERSION:
				if not warn_grapes: warn_grapes = True
				print(f"[grapes] CRITICAL | Table \"{self.__tables[table].Name}\" was made with grapes version {self.__tables[table].GRAPES_VERSION} but you're running {GRAPES_VERSION}!")
			if self.__tables[table].PYTHON_VERSION != PYTHON_VERSION:
				if not warn_python: warn_python = True
				print(f"[grapes] CRITICAL | Table \"{self.__tables[table].Name}\" was made with python version {self.__tables[table].PYTHON_VERSION} but you're running {PYTHON_VERSION}!")
		if warn_grapes:
			print("[grapes] CRITICAL | Re-making Any out-dated tables with your current grapes version is recommended! If you don't know how, feel free to ask!")
			if not self.__force_through_warnings:
				raise Exception("Execution cannot continue for your own safety.\n\nTIP: If you want to proceed Anyways, pass in argument \"force_through_warnings\" as true when initializing the database.")
		if warn_python:
			print("[grapes] CRITICAL | Different python versions can interpret things differently! You could suffer from potential data loss if you don't re-make the table for this version of switch to the table's version")
			if not self.__force_through_warnings:
				raise Exception("Execution cannot continue for your own safety.\n\nTIP: If you want to proceed Anyways, pass in argument \"force_through_warnings\" as true when initializing the database.")
	
	def __generate_files(self,dir_structure:dict) -> None:
		for parent, children in dir_structure.items():
			if not os.path.exists(parent):
				os.mkdir(parent)
			if isinstance(children,dict):
				self.__generate_files(children)
			elif not os.path.exists(children):
				os.mkdir(children)
	
	def __update_definition(self) -> None:
		with open(f"{self.__tables_dir}/definition.bin","rb") as file:
			self.__tables:dict = pickle.load(file)
	
	def __upgrade_definition(self) -> None:
		with open(f"{self.__tables_dir}/definition.bin","wb") as file:
			pickle.dump(self.__tables,file)
	
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
			if special_char in table.Name:
				raise TableError.TableNameIsBlankOrInvalid(f"You cannot use special characters in the table name! ({special_char})")
		if len(table.Columns) == 0:
			raise TableError.TableHasNoColumns(f"Tables must have at least one (1) column in order to be created.")
		self.__tables[table.Name] = table
		self.__upgrade_definition()
		with open(f"{self.__tables_dir}/{table.Name}.grape","wb") as file:
			pickle.dump([],file)
	
	def delete_table(self,table_name:str) -> None:
		if table_name not in self.__tables:
			raise TableError.TableDoesNotExist(f"No table named \"{table_name}\" could be found or exists in the database.")
		os.remove(f"{self.__tables_dir}/{table_name}.grape")
		del self.__tables[table_name]
		self.__upgrade_definition()
	
	def has_table(self,table_name:str) -> bool:
		return table_name in self.__tables
	
	def insert_into(self,table_name:str,values:tuple[Any,...]) -> None:
		if table_name not in self.__tables:
			raise InsertError.TableNotFound(f"No table named \"{table_name}\" could be found or exists in the database.")
		if len(values) == 0:
			raise InsertError.EmptyRequest("At least one (1) value must be provided in the insert request.")
		if len(values) > len(self.__tables[table_name].Columns):
			raise InsertError.ExtraValue("The insert request has more values than the table has columns.")
		self.__tables[table_name].Last += 1
		self.__upgrade_definition()
		with open(f"{self.__tables_dir}/{table_name}.grape","rb") as file:
			data:list[Union[tuple[Any,...],None]] = pickle.load(file)
		for index, column in enumerate(self.__tables[table_name].Columns):
			if len(values) < index+1:
				values += (column.DefaultValue,)
			if type(values[index]) != column.OfType:
				raise InsertError.TypeError("Inserted value must be of matching type to column's allowed type. (i.e. str==str, int!=str)")
		data.append(values)
		with open(f"{self.__tables_dir}/{table_name}.grape","wb") as file:
			pickle.dump(data,file)
	
	def get_all(self,table_name:str) -> list[tuple[Any,...]]:
		if table_name not in self.__tables:
			raise GetError.TableNotFound(f"No table named \"{table_name}\" could be found or exists in the database.")
		with open(f"{self.__tables_dir}/{table_name}.grape","rb") as file:
			data:list[tuple[Any,...]] = pickle.load(file)
		return data

	def get_where(self,table_name:str,column_name:str,is_equal_to:Any) -> Union[tuple[Any,...]]:
		if table_name not in self.__tables:
			raise GetError.TableNotFound(f"No table named \"{table_name}\" could be found or exists in the database.")
		data:list[tuple[Any,...]] = self.get_all(table_name)
		for row in data:
			for index, column in enumerate(self.__tables[table_name].Columns):
				if column.Name != column_name:
					continue
				if row[index] == is_equal_to:
					return row
		return ()

	def get_all_where(self,table_name:str,column_name:str,is_equal_to:Any) -> list[tuple[Any,...]]:
		if table_name not in self.__tables:
			raise GetError.TableNotFound(f"No table named \"{table_name}\" could be found or exists in the database.")
		data:list[tuple[Any,...]] = self.get_all(table_name)
		to_return:list[tuple[Any,...]] = []
		for row in data:
			for index, column in enumerate(self.__tables[table_name].Columns):
				if column.Name != column_name:
					continue
				if row[index] == is_equal_to:
					to_return.append(row)
		return to_return
