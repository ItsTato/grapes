from grapes import Database, Column, Types

db:Database = Database()

if not db.has_table("Users"):
	db.create_table("Users",columns=[
		Column("ID",Types.INTEGER,0,True),
		Column("Name",Types.STRING,"",False),
		Column("Robux",Types.INTEGER,0,False)
	])
