#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET'])
def bakeries():
    if request.method == 'GET':
        bakeries = Bakery.query.all()
        bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

        response = make_response(
            bakeries_serialized,
            200
        )
        return response

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    if request.method == 'GET':
        bakery = Bakery.query.filter_by(id=id).first()
        bakery_serialized = bakery.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response
    elif request.method == 'PATCH':
        bakery_to_update = Bakery.query.filter_by(id=id).first()
        
        for attr in request.form:
            setattr(bakery_to_update, attr, request.form.get(attr))
            
        db.session.add(bakery_to_update)
        db.session.commit()
        
        bakery_dict = bakery_to_update.to_dict()
        
        response = make_response(
            bakery_dict,
            200
        )
        return response
    
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods = BakedGood.query.all()
        baked_goods_serialized = [bg.to_dict() for bg in baked_goods]
        
        response = make_response(
            baked_goods_serialized,
            200
        )
        return response
    elif request.method == "POST":
        new_baked_good = BakedGood()
        for attr in request.form:
            setattr(new_baked_good, attr, request.form.get(attr))
        db.session.add(new_baked_good)
        db.session.commit()

        response = make_response(
            new_baked_good.to_dict(),
            201
        )
        return response 
    
@app.route('/baked_goods/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def baked_good_by_id(id):
    if request.method == 'GET':
        baked_good = BakedGood.query.filter_by(id=id).first()
        baked_good_serialized = baked_good.to_dict()

        response = make_response(
            baked_good_serialized,
            200
        )
        return response
    elif request.method == 'PATCH':
        baked_good_to_update = BakedGood.query.filter_by(id=id).first()
        
        for attr in request.form:
            setattr(baked_good_to_update, attr, request.form.get(attr))
            
        db.session.add(baked_good_to_update)
        db.session.commit()
        
        baked_good_dict = baked_good_to_update.to_dict()
        
        response = make_response(
            baked_good_dict,
            200
        )
        return response
    elif request.method == 'DELETE':
        baked_good_to_delete = BakedGood.query.filter_by(id=id).first()
        db.session.delete(baked_good_to_delete)
        db.session.commit()
        
        response = make_response(
            {'message': 'Baked good deleted'},
            200
        )
        return response
        

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
