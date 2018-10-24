from manage import DbSetup
db=DbSetup('testing')
def create():
    db.create_tables()
create()
