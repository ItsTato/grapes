from grapes import Database, Column, Types

db:Database = Database()

db.create_table("TestTable",columns=[
	Column("Robux",Types.INTEGER,0,False),
    Column("RAP",Types.FLOAT,32.6,False)
])
