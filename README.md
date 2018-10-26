
[![Build Status](https://travis-ci.org/charitymarani/store_manager_api_v2.svg?branch=Develop)](https://travis-ci.org/charitymarani/store_manager_api_v2)
[![Coverage Status](https://coveralls.io/repos/github/charitymarani/store_manager_api_v2/badge.svg?branch=Develop)](https://coveralls.io/github/charitymarani/store_manager_api_v2?branch=Develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/bf31b1530f6eec756f65/maintainability)](https://codeclimate.com/github/charitymarani/store_manager_api_v2/maintainability)
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
| POST     | /api/v2/products        | Add a product      |
| GET     | /api/v2/products       | Retrieve all products     |
| GET     | /api/v2/products/productId       | Retrieve a single product by id     |
| PUT    | /api/v2/products/productId       | Edit a  product record    |
| DELETE     | /api/v2/products/productId       | Deletes a product    |
| POST     | /api/v2/sales        | Post a new sale record     |
| GET     | /api/v2/sales        | Gets all sale records     |
| GET     | /api/v2/sales/saleid       |Gets a single sale by sale id       |



### Prerequisites
```
  * pip
  * virtualenv
  * python 3 or python 2.7
  * postgresql
  * PgAdmin (Optional)
```
### Setting up database
#### To create the databases through the command line:
  ```
  $ psql postgres
  postgres=# CREATE DATABASE store_manager
  postgres=# CREATE DATABASE test_store_db
  
  ```
 ### Alternatively use PgAdmin:
  Open Postgres PgAdmin and create 2 databases test_store_db and store_manager
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
