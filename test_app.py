import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *


class GymTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "gym"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Test variables
        # TOKENS
        self.manager = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9GV0FUSUNLTTdWNUg2emlMU1dPZCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRraG9sb29kLmF1dGgwLmNvbS8iLCJzdWIiOiJnb29nbGUtb2F1dGgyfDExMjYzMzg5ODEwNTU0MTc5MzE2NCIsImF1ZCI6WyJneW0iLCJodHRwczovL2ZzbmRraG9sb29kLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1OTg2MTYyMjIsImV4cCI6MTU5ODcwMjYyMiwiYXpwIjoiamNlNmVPb1QxenpYbHZKZzNOMmM5RktvRk03dXdlUmkiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNsYXNzZXMiLCJkZWxldGU6cm9vbXMiLCJkZWxldGU6dHJhaW5lcnMiLCJnZXQ6Y2xhc3NlcyIsImdldDpyb29tcyIsImdldDp0cmFpbmVycyIsInBhdGNoOmNsYXNzZXMiLCJwYXRjaDp0cmFpbmVycyIsInBvc3Q6Y2xhc3NlcyIsInBvc3Q6cm9vbXMiLCJwb3N0OnRyYWluZXJzIl19.IFnhTqCV_9niQfxITruD6t6c4F561jSQUXVL8SlWMQHfIbZxHwi27A4U2HW3nRAAEthK4f7JWTnF_6XsLw8kwTZF701fxNBmtJIb-HnhSerJBANLY7G8M0cOfepL0fpFaaKiq6SrRyzF6fZUWw-fN-i4AAGtVghUl7MiypKjVFJvOe3zfMOAUF-Mj6v_MgOnJwvCLkyWrf-pJHJRMu7_SkxSFm6RykZpRnUIvkHqVZu1AICt-Lrz8fPVgyRkF5qiccs5w_pim-LPIsBgBLlGmGp3ijyA5gnBIbz8E7wVEp9QCbzz_kiGboTl4aWamkkY0Gy9j7ysemCuQ_2ktGylbA'
        self.trainer = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9GV0FUSUNLTTdWNUg2emlMU1dPZCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRraG9sb29kLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWYzYmM3OWE3YzNjNTAwMTlkNjNjMjUiLCJhdWQiOiJneW0iLCJpYXQiOjE1OTg1NzAxOTgsImV4cCI6MTU5ODY1NjU5OCwiYXpwIjoiamNlNmVPb1QxenpYbHZKZzNOMmM5RktvRk03dXdlUmkiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpjbGFzc2VzIiwiZ2V0OmNsYXNzZXMiLCJnZXQ6cm9vbXMiLCJnZXQ6dHJhaW5lcnMiLCJwYXRjaDpjbGFzc2VzIiwicG9zdDpjbGFzc2VzIl19.TB1fgPXaaqcHX1DHYoiIYU5uEW5U0POMiCjH1TEimjHumA2pxXyTkKIWH5ZtOZEi0RCBjttKV-Weny4mdvFlObYmsoxb5YzZapz2tYSMzDmLm5z9dqqGdPZlyuC5RoQMivjTiJG6DVK4wd7eRdlEQsxpa6-M7GND9cz6VTnclsIFRJXQsfU_SSfjtDWHyUp5Q9HlwToBs-epWDoco1ova7VANiNtpa2c66UKPWzGHCrxLaIp6JYeKRDOEgIfvEW8oJxIMQyu8jlk0NJ0RwaUcyf-EptNEHXXsQp1qmWe82BvFVJLx-pQzMj7NkXcgCEOiQOtkWeU1kSGs1C4WDDV7w'
        self.invalidToken = 'InvalidToken'


    def tearDown(self):
        """Executed after reach test"""
        pass





#TEST: Posting a new class
    def test_post_class_with_valid_token(self):
        res = self.client().post('/classes', headers={"Authorization": "Bearer {}".format(self.manager)},
            json={"class_id":"6","trainer_id":"1","room_id":"1","name":"Yoga","start_time": "2020-01-09 11:00:00"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_post_class_with_invalid_token(self):
        res = self.client().post('/classes', headers={"Authorization": "Bearer {}".format(self.invalidToken)},
            json={"class_id":"8","trainer_id":"1","room_id":"1","name":"Yoga","start_time": "2020-01-09 03:00:00"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized access')

    def test_405_for_missing_info(self):
        res = self.client().post('/classes',headers={"Authorization": "Bearer {}".format(self.manager)},
            json={"class_id": "11","room_id":"1","name":"Yoga","start_time": "2020-01-09 11:00:00"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

#TEST: Editing a class
    def test_patch_class(self):
        res = self.client().patch('/classes/1',headers={"Authorization": "Bearer {}".format(self.trainer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_if_class_does_not_exist(self):
        res = self.client().patch('/classes/1000',headers={"Authorization": "Bearer {}".format(self.trainer)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resourse is not found')


#TEST: Deleting a class
    def test_delete_class(self):
        res = self.client().delete('/classes/1',headers={"Authorization": "Bearer {}".format(self.manager)})
        data = json.loads(res.data)
        gym_class = classes.query.filter(classes.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(gym_class, None)

    def test_404_if_class_does_not_exist(self):
        res = self.client().delete('/classes/1000',headers={"Authorization": "Bearer {}".format(self.manager)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resourse is not found')

#TEST: Posting a new trainer
    def test_post_class(self):
        res = self.client().post('/trainers',headers={"Authorization": "Bearer {}".format(self.manager)},  json={"name":"Samar","phone":"87867869"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_post_trainer_with_invalid_token(self):
        res = self.client().post('/trainers', headers={"Authorization": "Bearer {}".format(self.invalidToken)},
            json={"name":"Mona","phone": "20200109"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized access')

    def test_405_for_missing_info(self):
        res = self.client().post('/trainers', headers={"Authorization": "Bearer {}".format(self.manager)}, json={"name":"","phone":"8587800"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

#TEST: Editing a trainer
    def test_patch_trainer(self):
        res = self.client().patch('/trainers/1',headers={"Authorization": "Bearer {}".format(self.manager)})
        data = json.loads(res.data)
        trainer = trainers.query.filter(trainers.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(trainer, None)

    def test_404_if_trainer_does_not_exist(self):
        res = self.client().patch('/trainers/1000',headers={"Authorization": "Bearer {}".format(self.manager)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resourse is not found')

#TEST: Deleting a trainer
    def test_delete_trainer(self):
        res = self.client().delete('/trainers/1',headers={"Authorization": "Bearer {}".format(self.manager)})
        data = json.loads(res.data)
        trainer = trainers.query.filter(trainers.id == 1).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(trainer, None)

    def test_404_if_trainer_does_not_exist(self):
        res = self.client().delete('/trainers/1000',headers={"Authorization": "Bearer {}".format(self.manager)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resourse is not found')

    #TEST: Posting a new room
    def test_post_room(self):
        res = self.client().post('/rooms',headers={"Authorization": "Bearer {}".format(self.manager)}, json={"id":"9","name":"S11"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_post_room_with_invalid_token(self):
        res = self.client().post('/rooms', headers={"Authorization": "Bearer {}".format(self.invalidToken)}, json={"id":"10","name":"S12"})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unauthorized access')

    def test_405_for_missing_info(self):
        res = self.client().post('/rooms',headers={"Authorization": "Bearer {}".format(self.manager)},json={"id":"11","name": ""})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method is not allowed')

#TEST: Deleting a room
    def test_delete_room(self):
        res = self.client().delete('/rooms/1',headers={"Authorization": "Bearer {}".format(self.manager)})
        room = rooms.query.filter(rooms.id == 1).one_or_none()
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(room, None)

    def test_404_if_room_does_not_exist(self):
        res = self.client().delete('/rooms/1000',headers={"Authorization": "Bearer {}".format(self.manager)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resourse is not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

