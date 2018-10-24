# store_manager_api_v2
Store Manager api is a simple flask api that powers  a web application that helps store owners manage sales and product inventory records.Version 2 uses postgresql database to store data.
### Available Endpoints:
| Http Method | Endpoint Route | Endpoint Functionality |
| :---         |     :---       |          :--- |
| POST   | /api/v2/register     | Creates a user account    |
| POST     | /api/v2/login        | Login a user      |
| POST     | /api/v2/logout       | Logout a user      |
| GET     | /api/v2/users        | Gets all users     |
| GET     | /api/v2/users/username       |Gets a single user by username       |


### Prerequisites
```
  * pip
  * virtualenv
  * python 3 or python 2.7
```
### Installation
clone the repo

``` 
git clone https://github.com/charitymarani/store_manager_api_v2.git

```

create a virtual environment

```
virtualenv <environment name>

```

activate the environment:

```
$source <Your env name>/bin/activate

```
install dependencies:

```
$pip install -r requirements.txt

```

Run the app, and your ready to go!

```
python run.py

```
### Running the tests
The tests have beene written using the python module unittests. The path to tests folder is `tests` . Use a test framework like nose to run the tests.
To run the tests use the command:

```
nosetests tests

```