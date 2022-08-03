
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, car_schemas

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/newcar', methods = ['POST'])
@token_required
def create_contact(current_user_token):
    make = request.json['make']
    model = request.json['_model']
    year = request.json['year']
    vin = request.json['vin']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make, model, year, vin, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/seecars', methods = ['GET'])
@token_required
def see_cars(current_user_token):
    u = current_user_token.token
    data = Car.query.filter_by(user_token = u).all()
    response = car_schemas.dump(data)
    return jsonify(response)

@api.route('/seecar/<id>', methods = ['get'])
@token_required
def get_single_contact(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/updatecar/<id>', methods = ['get', 'put'])
@token_required
def update(current_user_token, id):
    car = Car.query.get(id)
    car.make = request.json['make']
    car._model = request.json['_model']
    car.year = request.json['year']
    car.vin = request.json['vin']
    car.user_token = current_user_token.token

    db.session.commit()
    return jsonify(car_schema.dump(car))

@api.route('/delcar/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)