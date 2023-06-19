#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Owner, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the pet/owner directory!</h1>',
        200
    )
    return response


@app.route('/pets/<int:id>')
def pet_by_id(id):
    pet = Pet.query.filter_by(id=id).first()
    response_body = make_response(f'''
                             
        <h1> Information for '{pet.name} the {pet.species}'</h1>
        <h2>Pet species is {pet.species}</h2>
        <h2>Pet Owner is '{pet.owner.name}'</h2>
    ''')
    response = make_response(response_body, 200)
    return response


@app.route('/owner/<int:id>')
def owner_by_id(id):
    owner = Owner.query.filter_by(id=id).first()

    if not owner:
        response_body = f'Person does not exist'
        response = make_response(response_body, 400)
        return response

    response_body = f'<h1>Information for {owner.name}</h1>'

    # creates a new list rather than modifying the original
    pets = [pet for pet in owner.pets]

    if not pets:
        response += f'<h2>{owner} has no pets</h2>'
    else:
        for pet in pets:
            response_body += f'<h2>Has pet {pet.species} named {pet.name}.</h2>'

    response = make_response(response_body, 200)
    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
