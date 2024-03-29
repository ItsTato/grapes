import pickle, time
from threading import Thread
from typing import Union

from .Errors import InsertError, GetError
from .Types import any
from .Table import Table
from .GrapesDatabase import GrapesDatabase

class InMemoryDatabase(GrapesDatabase):
	def __init__(self,data_directory:str="/data",write_rate:float=120.0) -> None:
		super().__init__(data_directory=data_directory)
		self.__table_data:dict = {}
		self.__write_rate:float = write_rate
		self.__modified_tables:list=[]
		self.__update_tables()
		self.__upgrade_thread:Thread = Thread(target=self.__write_data_thread)
		self.__upgrade_thread.daemon = True
		self.__upgrade_thread.start()
		return
	
	def __update_tables(self) -> None:
		for table in self.__tables:
			with open(f"{self.__tables_dir}/{table}.grape","rb") as file:
				self.__table_data[table] = pickle.load(file)
				file.close()
		return

	def __upgrade_tables(self) -> None:
		for table in self.__modified_tables:
			self.__modified_tables.remove(table)
			with open(f"{self.__tables_dir}/{table}.grape","wb") as file:
				pickle.dump(self.__table_data[table],file)
				file.close()
		return
	
	def __write_data_thread(self) -> None:
		while True:
			time.sleep(self.__write_rate)
			self.__upgrade_definition()
			self.__upgrade_tables()
	
	def create_table(self,table:Table) -> None:
		super().create_table(table)
		self.__table_data[table.Name] = []
		return
	
	def delete_table(self, table_name: str) -> None:
		super().delete_table(table_name)
		del self.__table_data[table_name]
		if table_name in self.__modified_tables:
			self.__modified_tables.remove(table_name)
		return
	
	def insert_into(self,table_name:str,values:tuple[any,...]) -> None:
		if table_name not in self.__tables:
			raise InsertError.TableNotFound(f"No table with the name \"{table_name}\' could be found.")
		if len(values) == 0:
			raise InsertError.EmptyRequest("At least one (1) value must be provided in the request.")
		if len(values) > len(self.__tables[table_name].Columns):
			raise InsertError.ExtraValue("The request has more values than the table has columns.")
		self.__tables[table_name].Last += 1
		if len(values) != len(self.__tables[table_name].Columns):
			for index, column in enumerate(self.__tables[table_name].Columns):
				if len(values) < index+1:
					values += (column.DefaultValue,)
		self.__table_data[table_name].append(values)
		self.__modified_tables.append(table_name)
		return
	
	def get_all(self,table_name:str) -> list[Union[tuple,None]]:
		if table_name not in self.__tables:
			raise GetError.TableNotFound(f"No table with the name \"{table_name}\' could be found.")
		return self.__table_data[table_name]
