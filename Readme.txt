FSND-Capstone-Project
Udacity Fullstack Nanodegree capstone project

the api is deployed on
https://kholoodgym.herokuapp.com/

You can access the endpoints using the following tokens:
Manager:
Trainer:


This project includes creating an api that serves a gym website by providing a set of endpoints to access the gym rooms, trainers and the classes.
Some endpoints that inncludes modifying the data requires authorized access. In this project, Auth0 service iss used for identity check.
Getting Started
Requirements

Install the necessary requirmenets by running:

    pip install -r requirements.txt
Running on local machine

Open a terminal and cd to the project directory and install requirements:
    cd ~/FSND-Capstone-Project
    # Then
    pip install -r requirements.txt
Set up your DATABASE_URL variable depending on OS:
    $env:DATABASE_URL="{DATABASE_URL}"

Set up Authentication with Auth0.com. You need two roles with different permissions:
1-Manager
permissions:
    get:classes
    post:classes
    patch:classes
    delete:classes
    get:trainers
    post:trainers
    patch:trainers
    delete:trainers
    get:rooms
    post:rooms
    delete:rooms
2-Trainer
permissions:
    get:classes
    post:classes
    patch:classes
    delete:classes
    get:rooms
    get:trainers

Set up FLASK_APP variable depending on OS:
     $env:FLASK_APP="app.py"
To run the app use:
    flask run
By default, the app will run on http://127.0.0.1:5000/
Endpoints and Error Handlers
ENDPONTS

GET '/classes'
POST '/classes'
PATCH '/classes/int:id'
DELETE '/classes/int:id'

GET '/trainers'
POST '/trainers'
PATCH '/trainers/int:id/'
DELETE '/trainers/int:id'

GET '/rooms'
POST '/rooms'
DELETE '/rooms/int:id'

GET '/classes'
- No Authorization required
- Gets all the classes in the database
- Returns
    {
        'success': True,
        'classes': [{
            "room_id": self.room_id,
            "room_name": rooms.name,
            "start_time": self.start_time,
            "trainer_id": self.trainer_id,
            "trainer_name": trainers.name
}

POST '/classes'
- Reqiured Authorization with 'Manager' and 'Trainer' role
- Add new class
- Returns:
    {
        'success': True,
        'classes' = {"id":classes.id,
            "name":classes.name ,
            "trainer_id":classes.trainer_id,
            "room_id":classes.room_id,
            "start_time":classes.start_time}]
    }

PATCH '/classes/int:id'
- Reqiured Authorization with 'Manager' and 'Trainer' role
- Modify certain class
- Returns:
    {
        'success': True,
        'classes' = {"id":classes.id,
            "name":classes.name ,
            "trainer_id":classes.trainer_id,
            "room_id":classes.room_id,
            "start_time":classes.start_time}]
    }

DELETE '/classes/int:id'
- Reqiured Authorization with 'Manager' and 'Trainer' role
-Delete certain class
- Returns :
    {
        'success': True, 'class_id': class_id
    }


GET '/trainers'
- No Authorization required
- Gets all the trainers in the database
- Returns
    {
        'success': True,
        'all_trainers': {
            "id":self.id,
            "name":self.name ,
            "phone":self.phone
    }
POST '/trainers'
- Reqiured Authorization with 'Manager' role
- Create new trainer
- Returns:
   {
        'success': True,
        'all_trainers': {
            "id":self.id,
            "name":self.name ,
            "phone":self.phone
    }

PATCH '/trainers/<int:id>'
- Requred Authorization with ' Manager' role
- Modify certain trainer
- Returns:
    {
        'success': True,
        'trainer': {
            "id":self.id,
            "name":self.name ,
            "phone":self.phone
    }


DELETE '/trainers/<int:id>'
- Reqiured Authorization with 'Manager' role
- Delete certain trainer
- Returns:
    {
        "success": True,
        'trainer_id': self.id
    }


GET '/rooms'
- No Authorization required
- Gets all the trainers in the database
- Returns
    {
        'success': True,
        'rooms': [{
            "id": self.id,
            "name": self.name,
    }
POST '/rooms'
- Reqiured Authorization with 'Manager' role
- Create new trainer
- Returns:
    {
        "success": True,
        "rooms": {
            "id": self.id,
            "name": self.name
    }

DELETE '/rooms/<int:id>'
- Reqiured Authorization with 'Manager' role
- Delete certain trainer
- Returns:
    {
        "success": True,
        'id':self.id
    }


ERROR HANDLERS

Error 422 (Unprocessable)
Returns:
   {"success": False, "error": 422, "message": "Unprocessable"}

Error 404 (Resourse is not found)
Returns:
    {"success": False, "error": 404, "message": "Resourse is not found"}


Error 400 (Bad request)
Returns:
    {"success": False, "error": 400, "message": "Bad request"}

Error 405 (Method is not allowed)
Returns:
    {"success": False, "error": 405, "message": "Method is not allowed"}

Error 500 (Internal server error)
Returns:
    {"success": False,  "error": 500, "message": "Internal server error"}

Authentication
You can securly Sign Up or Log In through Auth0: https://fsndkholood.auth0.com/authorize?audience=gym&response_type=token&client_id=jce6eOoT1zzXlvJg3N2c9FKoFM7uweRi&redirect_uri=https://kholoodgym.herokuapp.com/


Authors
Kholood Awad

