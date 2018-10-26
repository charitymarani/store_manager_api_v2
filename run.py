'''./run.py'''

from application import create_app
from manage import DbSetup


CONFIG_NAME = "development"
app = create_app(CONFIG_NAME)
db=DbSetup()


@app.route('/')
def home():
    '''method for home page'''
    return "<h2>Welcome to store manager api version 2</h2>"

if __name__ == "__main__":
    db.create_tables()
    app.run()
