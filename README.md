# Real-Estate-Development-Platform API

## About 

The Project is developed for a Real Estate Company. The website contains list of building, where admin can create, read, update and delete building on the website while the owners can see the details of their own buildings.

https://real-estate-platform-altwaim.herokuapp.com/

## API
Everyone can see the list of buidling and units we have but you need to be authenticated to do the any thing else. There are two type of users "Admin and Owner" where the Owner can see the detail of an indvidual building and Admin can do all of it including create, read, update and delete building.

## Retrieves a building info(Everyone)
**GET** `/buildings`

``` 
curl -X GET \https://real-estate-platform-altwaim.herokuapp.com/buildings\ -H

```
## Retrieves a building by its id(admin&owner)
**GET** `/buildings/<id>`

```
curl -X GET \https://real-estate-platform-altwaim.herokuapp.com/buildings/2\ -H 'Authorization: Bearer <Your_Token>'

```

## Create a new building (Only Admin)
**POST** `/buildings`

```
curl -X POST \https://real-estate-platform-altwaim.herokuapp.com/buildings\ -H 'Authorization: Bearer <Your_Token>' \
-H 'Content-Type: application/json' \
-d '{
    "address": "Alyasmin",
    "description": "3 floors building",
    "name": "Tlal",
    "number_of_units": 9,
    "ownerID": 1234567890,
    "building_image": "https://dangerwordfilm.files.wordpress.com/2014/04/coming-soon.png"
}'

```

## Update a buidling (only admin)
**PATCH** `/buildings/<id>`

```
curl -X PATCH \https://real-estate-platform-altwaim.herokuapp.com/buildings/2\ -H 'Authorization: Bearer <Your_Token>' \
-H 'Content-Type: appliction/json' \
-d '{
    "address": "Almraba"
}'

```

## Delete a building (only admin)
**DELETE** `/buildings/<id>`

```
curl -X DELETE \https://real-estate-platform-altwaim.herokuapp.com/buildings/4\ -H 'Authorization: Bearer <Your_Token>'

```

## Retrieves units by its building id(Everyone)
**GET** `/buildings/<id>/units`

``` 
curl -X GET \https://real-estate-platform-altwaim.herokuapp.com/buildings/2/units\ -H

```

## Installation

How to install and run the project locally.

1- Install the dependencies:
The project requires Python 3.8 and using virtual environment.
```
pipenv shell
pipenv install
pip3 install -r requirements.txt
```
2- Database Setup:
```
Create a database name: estate
 change app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://<Your_User>@localhost:5432/estate'
```
3- Run the development server:

On Linux or Mac: export 
```
$ export FLASK_APP=app
$ export FLASK_ENV=development
$ FLASK_APP=app flask run
```
On Windows: set 
```
$ set FLASK_APP=app
$ set FLASK_ENV=development
$ FLASK_APP=app flask run
```

4- Navigate to Home page [http://localhost:5000](http://localhost:5000)


## Data Modeling
The schema for the database and helpers methods to simplify API are in models.py
- There are two tables created: Building and Unit.
- The Building table are used by everyone to retrieve existing buildings and by admin to add new building and their informations, update or delete them.
- The Unit table is used to add new units and thier informations.
- The Unit table has a foreign key on the Building table for building_id.
- Each table has an insert, update, delete, and format helper functions.