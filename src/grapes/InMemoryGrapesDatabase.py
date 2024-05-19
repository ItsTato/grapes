import pickle, time
from threading import Thread
from typing import Union, Any

from .Errors import InsertError, GetError
from .Table import Table
from .GrapesDatabase import GrapesDatabase

class InMemoryGrapesDatabase(GrapesDatabase):
	def __init__(self,file_loc:str,data_directory:str="./data",write_rate:float=120.0,force_through_warnings:bool=False) -> None:
		super().__init__(file_loc=file_loc,data_directory=data_directory,force_through_warnings=force_through_warnings)
		self.__table_data:dict[str,list[tuple[Any,...]]] = {}
		self.__write_rate:float = write_rate
		self.__modified_tables:list[str]=[]
		self.__update_tables()
		self.__upgrade_thread:Thread = Thread(target=self.__write_data_thread)
		self.__upgrade_thread.daemon = True
		self.__upgrade_thread.start()

	def __update_tables(self) -> None:
		for table in self._GrapesDatabase__tables:
			with open(f"{self._GrapesDatabase__tables_dir}/{table}.grape","rb") as file:
				self.__table_data[table] = pickle.load(file)

	def __upgrade_tables(self) -> None:
		for table in self.__modified_tables:
			self.__modified_tables.remove(table)
			with open(f"{self._GrapesDatabase__tables_dir}/{table}.grape","wb") as file:
				pickle.dump(self.__table_data[table],file)

	def __write_data_thread(self) -> None:
		while True:
			time.sleep(self.__write_rate)
			self._GrapesDatabase__upgrade_definition()
			self.__upgrade_tables()

	def write_all_data(self) -> None:
		self._GrapesDatabase__upgrade_definition()
		self.__upgrade_tables()

	def create_table(self,table:Table) -> None:
		super().create_table(table)
		self.__table_data[table.Name]:list[tuple[Any,...]] = []

	def delete_table(self, table_name: str) -> None:
		super().delete_table(table_name)
		del self.__table_data[table_name]
		if table_name in self.__modified_tables:
			self.__modified_tables.remove(table_name)

	def insert_into(self,table_name:str,values:tuple[Any,...]) -> None:
		if table_name not in self._GrapesDatabase__tables:
			raise InsertError.TableNotFound(f"No table named \"{table_name}\" could be found or exists in the database.")
		if len(values) == 0:
			raise InsertError.EmptyRequest("At least one (1) value must be provided in the insert request.")
		if len(values) > len(self._GrapesDatabase__tables[table_name].Columns):
			raise InsertError.ExtraValue("The insert request has more values than the table has columns.")
		self._GrapesDatabase__tables[table_name].Last += 1
		if len(values) != len(self._GrapesDatabase__tables[table_name].Columns):
			for index, column in enumerate(self._GrapesDatabase__tables[table_name].Columns):
				if len(values) < index+1:
					values += (column.DefaultValue,)
		self.__table_data[table_name].append(values)
		self.__modified_tables.append(table_name)

	def get_all(self,table_name:str) -> list[tuple[Any,...]]:
		if table_name not in self._GrapesDatabase__tables:
			raise GetError.TableNotFound(f"No table named \"{table_name}\" could be found or exists in the database.")
		return self.__table_data[table_name]

	def get_where(self,table_name:str,column_name:str,is_equal_to:Any) -> Union[tuple[Any,...]]:
		if table_name not in self._GrapesDatabase__tables:
			raise GetError.TableNotFound(f"No table named \"{table_name}\" could be found or exists in the database.")
		for row in self.__table_data[table_name]:
			for index, column in enumerate(self._GrapesDatabase__tables[table_name].Columns):
				if column.Name == column_name and row[index] == is_equal_to:
					return row
		return ()

	def get_all_where(self,table_name:str,column_name:str,is_equal_to:Any) -> list[tuple[Any,...]]:
		if table_name not in self._GrapesDatabase__tables:
			raise GetError.TableNotFound(f"No table named \"{table_name}\" could be found or exists in the database.")
		to_return:list[tuple[Any,...]] = []
		for row in self.__table_data[table_name]:
			for index, column in enumerate(self._GrapesDatabase__tables[table_name].Columns):
				if column.Name == column_name and row[index] == is_equal_to:
					to_return.append(row)
					break
		return to_return
