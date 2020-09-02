import os
from sqlalchemy import Column, String, create_engine, Integer, DateTime, Numeric, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

#database_path = os.environ['DATABASE_URL']
database_name = "gym"
database_path = "postgres://{}:{}@{}/{}".format('postgres','postgres','localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class rooms(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key = True , nullable = False)
    name = db.Column(db.String() , nullable = False)
    classes = db.relationship('classes', backref="rooms",cascade="all, delete-orphan", lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class trainers(db.Model):
    __tablename__ = 'trainers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),nullable=False)
    phone = db.Column(db.Text)
    classes = db.relationship('classes', backref="trainers",cascade="all, delete-orphan", lazy=True)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return { 'id': self.id , 'name': self.name ,'phone': self.phone}

class classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer , primary_key=True , nullable=False)
    name = db.Column(db.String , nullable=False)
    trainer_id = db.Column(db.Integer , db.ForeignKey('trainers.id') , nullable=False)
    room_id = db.Column(db.Integer , db.ForeignKey('rooms.id') , nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return { 'id': self.id , 'name': self.name,'trainer_id': self.trainer_id,'room_id': self.room_id ,'start_time': self.start_time}
