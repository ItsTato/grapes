from grapes import GrapesDatabase, Table, Column

db:GrapesDatabase = GrapesDatabase(__file__)

if not db.has_table("Users"):
	db.create_table(Table(
		"Users",
		columns=[
			Column("ID",int,0,True),
			Column("Name",str,"",False),
			Column("Robux",int,0,False)
		]
	))

db.insert_into("Users",(1,"Tato",400))
db.insert_into("Users",(2,"pelele",200))
db.insert_into("Users",(3,"ea_ea",-1200))

print(db.get_where("Users","ID",1))
print(db.get_where("Users","Name","pelele"))
print(db.get_where("Users","Robux",-1200))

print(db.get_all("Users"))

from grapes import InMemoryGrapesDatabase
db2:InMemoryGrapesDatabase = InMemoryGrapesDatabase(__file__,"./data2")

if not db2.has_table("Users"):
	db2.create_table(Table(
		"Users",
		columns=[
			Column("ID",int,0,True),
			Column("Name",str,"",False),
			Column("Robux",int,0,False)
		]
	))

db2.insert_into("Users",(22,"I exist!",7))
print(db2.get_all("Users"))
print(db2.get_where("Users","ID",22))

# With write rate 120.0s there's no chance
# of this data being written, so must do
# manually...
db2.write_all_data()
