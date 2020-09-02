'''------------------------Packages Imports ------------------------'''
import os
from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    abort,
    jsonify
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import func, select
from flask_migrate import Migrate
from models import *
from sqlalchemy import exc
import datetime
from auth import AuthError, requires_auth


'''------------------------App configuration ------------------------'''


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    db = SQLAlchemy(app)
    migrate=Migrate(app,db)
    # Set up CORS. Allow '*' for origins.
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow_Headers', 'ContentTyp , Authorization')
        response.headers.add('Access-Control-Allow_Methods', 'GET, POST , PATCH, DELETE ,OPTIONS')
        return response

    @app.route('/')
    def main_page():
        return "Welcom to the Gym api, go to readme file to try different endpoints"

    '''------------------------Classes ------------------------'''
    '''-------1-Display all the classes----'''
    @app.route('/classes', methods=['GET'])
    def get_classes():
        all_classes=[]
        all_classes1 = classes.query.join(trainers).join(rooms).all()
        for s in all_classes1:
            all_classes.append({
              "trainer_id":s.trainer_id,
              "trainer_name":s.trainers.name,
              "room_id":s.room_id,
              "room_name":s.rooms.name,
              "start_time":s.start_time})
        return jsonify({'success': True, 'classes': all_classes}), 200

    '''-------2-Creating a new class--'''
    @app.route('/classes', methods=['POST'])
    @requires_auth('post:classes')
    def create_class(token):
        try:
            body = request.get_json()
            class_id = body.get("class_id", None)
            class_trainer = body.get("trainer_id", None)
            class_room = body.get("room_id", None)
            class_name = body.get("name", None)
            start_time = body.get("start_time", None)
            if class_trainer or class_room or class_name or start_time is None:
                abort(405)
            gym_class = classes(id = class_id , trainer_id = class_trainer , room_id = class_room , name = class_name , start_time = start_time)
            gym_class.insert()
            new_gym_class1 = classes.query.get(class_id)
            new_gym_class2 = {"id":new_gym_class1.id,
            "name":new_gym_class1.name ,
            "trainer_id":new_gym_class1.trainer_id,
            "room_id":new_gym_class1.room_id,
            "start_time":new_gym_class1.start_time}
            return jsonify({'success': True, 'gym_class': new_gym_class2}), 200
        except:
            abort(405)

    '''-------3-Deleating a class--'''
    @app.route('/classes/<int:class_id>', methods=['DELETE'])
    @requires_auth('delete:classes')
    def delete_class(token , class_id):
        gym_class = classes.query.get(class_id)
        if gym_class is None:
            abort(404)
        gym_class.delete()
        return jsonify({'success': True, 'class_id': class_id}), 200


    '''-------4-Updating a class information ------------------------'''
    @app.route('/classes/<int:class_id>', methods=['PATCH'])
    @requires_auth('patch:classes')
    def update_classes(token , class_id):
        gym_class = classes().query.filter(classes.id == class_id).one_or_none()
        if gym_class is None:
            abort(404)
        else:
            body = request.get_json()
            new_name = body.get('name', None)
            new_trainer = body.get('trainer_id', None)
            new_room = body.get('room_id', None)
            new_time = body.get('start_time', None)
            if new_name :
                gym_class.name  =  new_name
            if  new_trainer :
                gym_class.trainer_id  = new_trainer
            if new_room :
                gym_class.room_id  =  new_room
            if  new_time :
                gym_class.start_time  = new_time

            gym_class.update()
            edited_class1 = classes.query.get(class_id)
            edited_class2 = {"id":edited_class1.id,"name":edited_class1.name ,"trainer_id":edited_class1.trainer_id,
            "room_id":edited_class1.room_id,
            "start_time":edited_class1.start_time}
            return jsonify({'success': True, 'trainer': edited_class2}), 200

    '''------------------------Trainers------------------------'''
    '''-------1-Display all the trainers ---'''
    @app.route('/trainers', methods=['GET'])
    def show_trainers():
        try:
            trainers1=trainers.query.all()
            all_trainers= []
            for a in trainers1:
                all_trainers.append({"id":a.id,"name":a.name ,"phone":a.phone})
            return jsonify({'success': True, 'trainer': all_trainers}), 200
        except:
            abort(422)


    '''-------2-Updating a trainer information ------------------------'''
    @app.route('/trainers/<trainer_id>', methods = ['PATCH'])
    @requires_auth('patch:trainers')
    def update_trainer(token , trainer_id):
        trainer = trainers().query.filter(trainers.id == trainer_id).one_or_none()
        if trainer is None:
            abort(404)
        else:
            body = request.get_json()
            new_name = body.get('name', None)
            new_phone = body.get('phone', None)
            if new_name :
                trainer.name  =  new_name
            if  new_phone :
                trainer.phone  = new_phone
            trainer.update()
            edited_trainer1 = trainers.query.get(trainer_id)
            edited_trainer2 = {"id":edited_trainer1.id,"name":edited_trainer1.name ,"phone":edited_trainer1.phone}
            return jsonify({'success': True, 'trainer': edited_trainer2}), 200

    '''-------3-Creating a new trainer ------------------------'''
    @app.route('/trainers', methods = ['POST'])
    @requires_auth('post:trainers')
    def new_trainer(token):
        body = request.get_json()
        name = body.get("name", None)
        phone = body.get("phone", None)
        if name is None:
            abort(405)
        new_trainer = trainers( name = name, phone = phone)
        new_trainer.insert()
        trainer = new_trainer.format()
        return jsonify({'success': True, 'trainer': [trainer]}), 200

    '''-------4-Deleating a trainer--'''
    @app.route('/trainers/<trainer_id>', methods=['DELETE'])
    @requires_auth('delete:trainers')
    def delete_trainer(token , trainer_id):
            trainer = trainers.query.get(trainer_id)
            if trainer is None:
                abort(404)
            trainer.delete()
            return jsonify({'success': True, 'trainer_id': trainer_id}), 200


    '''------------------------Rooms-----------------------'''
    '''-------1-Display all the rooms and its details---'''
    @app.route('/rooms', methods=['GET'])
    def show_rooms():
        try:
            rooms1 = rooms.query.all()
            all_rooms = []
            for a in rooms1:
                all_rooms.append({"id":a.id,"name":a.name})
            return jsonify({'success': True, 'rooms': all_rooms}) , 200
        except:
            abort(422)

    '''-------2-Searching for a room------------------------'''
    @app.route('/rooms', methods=['POST'])
    @requires_auth("post:rooms")
    def search_or_add_rooms(token):

        body = request.get_json()
        search_term = body.get('searchTerm',None)
        if search_term :
            results=rooms.query.filter(rooms.name.ilike(f'%{search_term}%')).all()
            results_rooms = []
            for room in results:
                results_rooms.append({"id":room.id,"name":room.name})
            return jsonify({'success': True, 'room': results_rooms}), 200
        else:
            room_id = body.get('id',None)
            room_name = body.get('name',None)
            if room_name == "" :
                abort(405)
            new_room = rooms( id = room_id , name = room_name)
            new_room.insert()
            rooms1 = rooms.query.all()
            all_rooms = []
            for a in rooms1:
                all_rooms.append({"id":a.id,"name":a.name})
            return jsonify({'success': True, 'rooms': all_rooms}) , 200


    '''-------3-Deleting a room by the id------------------------'''
    @app.route('/rooms/<int:room_id>', methods=['DELETE'])
    @requires_auth("delete:rooms")
    def show_room(token,room_id):
            room = rooms.query.get(room_id)
            if room is None :
                abort(404)
            room.delete()
            return jsonify({'success': True, 'room_id' : room_id}), 200


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Resourse is not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({"success": False, "error": 422, "message": "Unprocessable"}), 422

    @app.errorhandler(400)
    def not_found(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"success": False, "error": 401, "message": "Unauthorized access"}), 401

    @app.errorhandler(405)
    def methodnotallowed(error):
        return jsonify({"success": False, "error": 405, "message": "Method is not allowed"}), 405

    @app.errorhandler(500)
    def internalServerErrror(error):
        return jsonify({"success": False,  "error": 500, "message": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
