from app import db
from flask_sqlalchemy import SQLAlchemy
import json


class Building(db.Model):
    __tablename__ = 'building'
    id = db.Column(db.Integer, primary_key=True)
    ownerID = db.Column(db.Integer, nullable=False, default=1234567890)
    name = db.Column(db.String(120), default='No description')
    address = db.Column(db.String(500), default='No description')
    description = db.Column(db.String(500), default='No description')
    number_of_units = db.Column(db.Integer, nullable=False, default=6)
    building_image = db.Column(db.String(500), default='https://dangerwordfilm.files.wordpress.com/2014/04/coming-soon.png')
    units = db.relationship('Unit', back_populates='building')

    def __init__(self, ownerID, name, address, description, number_of_units, building_image):
        self.ownerID = ownerID
        self.name = name
        self.address = address
        self.description = description
        self.number_of_units = number_of_units
        self.building_image = building_image

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def show(self):
        return{
            'id': self.id,
            'ownerID': self.ownerID,
            'name': self.name,
            'address': self.address,
            'description': self.description,
            'number_of_units': self.number_of_units,
        }


class Unit(db.Model):
    __tablename__ = 'unit'
    id = id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), default='No description')
    number_of_bedroom = db.Column(db.Integer, nullable=False, default=1)
    number_of_living_room = db.Column(db.Integer, nullable=False, default=1)
    number_of_bathroom = db.Column(db.Integer, nullable=False, default=1)
    vacancy = db.Column(db.Boolean(), default=True)
    type_of_rental = db.Column(db.String(120), default='Year')
    rent_price = db.Column(db.Integer, nullable=False, default=1000)
    unit_image = db.Column(db.String(500), default='https://dangerwordfilm.files.wordpress.com/2014/04/coming-soon.png')
    building_id = db.Column(db.Integer, db.ForeignKey('building.id'), nullable=False)
    building = db.relationship('Building', back_populates='units')

    def __init__(self, description, number_of_bedroom, number_of_living_room, number_of_bathroom, vacancy, type_of_rental, rent_price, unit_image, building_id):
        self.description = description
        self.number_of_bedroom = number_of_bedroom
        self.number_of_living_room = number_of_living_room
        self.number_of_bathroom = number_of_bathroom
        self.vacancy = vacancy,
        self.type_of_rental = type_of_rental
        self.rent_price = rent_price
        self.unit_image = unit_image
        self.building_id = building_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def show(self):
        return{
            'id': self.id,
            'description': self.description,
            'number_of_bedroom': self.number_of_bedroom,
            'number_of_living_room': self.number_of_living_room,
            'number_of_bathroom': self.number_of_bathroom,
            'vacancy': self.vacancy,
            'type_of_rental': self.type_of_rental,
            'rent_price': self.rent_price,
            'unit_image': self.unit_image,
            'building_id': self.building_id,

        }
