from grapes import GrapesDatabase, Table, Column, Types

db:GrapesDatabase = GrapesDatabase()

if not db.has_table("Users"):
	db.create_table(Table(
		"Users",
		columns=[
			Column("ID",Types.INTEGER,0,True),
			Column("Name",Types.STRING,"",False),
			Column("Robux",Types.INTEGER,0,False)
		]
	))

db.insert_into("Users",(37,"Howdy",1))
print(db.get_all("Users"))

from grapes import InMemoryDatabase
db2:InMemoryDatabase = InMemoryDatabase("/data2")
