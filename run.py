'''./run.py'''

from application import create_app
from manage import DbSetup


CONFIG_NAME = "development"
app = create_app(CONFIG_NAME)



@app.route('/')
def home():
    '''method for home page'''
    return "<h2>Welcome to store manager api version 2</h2>"

db = DbSetup(CONFIG_NAME)
if __name__ == "__main__":
    app.run()
