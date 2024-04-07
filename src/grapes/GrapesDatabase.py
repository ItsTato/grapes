import os, pickle
from typing import Union

from .Table import Table
from .Errors import TableError, InsertError, GetError
from .Types import any
from .__meta import GRAPES_VERSION, PYTHON_VERSION

# Tato's Notes-To-Self #

# Use shutil for backup operations
# (it can handle big copies of folders easily)
# (same with compression)

class GrapesDatabase:
	def __init__(self,data_directory:str="/data",force_through_warnings:bool=False) -> None:
		self.__force_through_warnings:bool = force_through_warnings
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
		if os.path.exists(f"{self.__tables_dir}/definition.bin"):
			self.__update_definition()
		else:
			self.__upgrade_definition()
		warn_grapes:bool = False
		warn_python:bool = False
		for table in self.__tables:
			if table.GRAPES_VERSION != GRAPES_VERSION:
				if not warn_grapes: warn_grapes = True
				print(f"[grapes] CRITICAL | Table \"{table.Name}\" was made with grapes version {table.GRAPES_VERSION} but you're running {GRAPES_VERSION}!")
			if table.PYTHON_VERSION != PYTHON_VERSION:
				if not warn_python: warn_python = True
				print(f"[grapes] CRITICAL | Table \"{table.Name}\" was made with python version {table.PYTHON_VERSION} but you're running {PYTHON_VERSION}!")
		if warn_grapes:
			print("[grapes] CRITICAL | Re-making any out-dated tables with your current grapes version is recommended! If you don't know how, feel free to ask!")
			if not self.__force_through_warnings:
				raise Exception("Execution cannot continue for your own safety.")
		if warn_python:
			print("[grapes] CRITICAL | Different python versions can interpret things differently! You could suffer from potential data loss if you don't re-make the table for this version of switch to the table's version")
			if not self.__force_through_warnings:
				raise Exception("Execution cannot continue for your own safety.")
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
		return
	
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
			raise TableError.TableHasNoColumns(f"Tables must have at least one (1) column.")
		self.__tables[table.Name] = table
		self.__upgrade_definition()
		with open(f"{self.__tables_dir}/{table.Name}.grape","wb") as file:
			pickle.dump([],file)
			file.close()
		return
	
	def delete_table(self,table_name:str) -> None:
		if table_name not in self.__tables:
			raise TableError.TableDoesNotExist(f"No table with the name \"{table_name}\" exists.")
		os.remove(f"{self.__tables_dir}/{table_name}.grape")
		del self.__tables[table_name]
		self.__upgrade_definition()
		return
	
	def has_table(self,table_name:str) -> bool:
		return table_name in self.__tables
	
	def insert_into(self,table_name:str,values:tuple[any,...]) -> None:
		if table_name not in self.__tables:
			raise InsertError.TableNotFound(f"No table with the name \"{table_name}\" could be found.")
		if len(values) == 0:
			raise InsertError.EmptyRequest("At least one (1) value must be provided in the request.")
		if len(values) > len(self.__tables[table_name].Columns):
			raise InsertError.ExtraValue("The request has more values than the table has columns.")
		self.__tables[table_name].Last += 1
		self.__upgrade_definition()
		with open(f"{self.__tables_dir}/{table_name}.grape","rb") as file:
			data:list[tuple] = pickle.load(file)
			file.close()
		for index, column in enumerate(self.__tables[table_name].Columns):
			if len(values) < index+1:
				values += (column.DefaultValue,)
			if type(values[index]).__name__ != column.OfType.Name:
				raise InsertError.TypeError("Inserted value must be of matching type to column's type.")
		data.append(values)
		with open(f"{self.__tables_dir}/{table_name}.grape","wb") as file:
			pickle.dump(data,file)
			file.close()
		return
	
	def get_all(self,table_name:str) -> list[Union[tuple[any,...],None]]:
		if table_name not in self.__tables:
			raise GetError.TableNotFound(f"No table with the name \"{table_name}\" could be found.")
		with open(f"{self.__tables_dir}/{table_name}.grape","rb") as file:
			data:list[Union[tuple[any,...],None]] = pickle.load(file)
			file.close()
		return data

	def get_where(self,table_name:str,column_name:str,is_equal_to:any) -> Union[tuple[any,...],None]:
		if table_name not in self.__tables:
			raise GetError.TableNotFound(f"No table with the name \"{table_name}\" could be found.")
		data:list[Union[tuple[any,...],None]] = self.get_all(table_name)
		for row in data:
			for index, column in enumerate(self.__tables[table_name].Columns):
				if column.Name == column_name and row[index] == is_equal_to: # type: ignore
					return row
		return None

	def get_all_where(self,table_name:str,column_name:str,is_equal_to:any) -> list[Union[tuple[any,...],None]]:
		if table_name not in self.__tables:
			raise GetError.TableNotFound(f"No table with the name \"{table_name}\" could be found.")
		data:list[Union[tuple[any,...],None]] = self.get_all(table_name)
		to_return:list[Union[tuple[any,...],None]] = []
		for row in data:
			for index, column in enumerate(self.__tables[table_name].Columns):
				if column.Name != column_name:
					break
				if row[index] == is_equal_to: # type: ignore
					to_return.append(row)
					break
		return to_return
