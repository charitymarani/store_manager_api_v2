from manage import DbSetup
db=Dbsetup('testing')
def create():
    db.create_tables()
create()
