#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


# ---------------- GET ----------------
@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    return jsonify([b.to_dict() for b in bakeries]), 200


@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    return jsonify(bakery.to_dict()), 200


@app.route('/baked_goods', methods=['GET'])
def get_baked_goods():
    baked_goods = BakedGood.query.all()
    return jsonify([bg.to_dict() for bg in baked_goods]), 200


@app.route('/baked_goods/<int:id>', methods=['GET'])
def get_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    return jsonify(baked_good.to_dict()), 200


# ---------------- POST ----------------
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.form
    new_baked_good = BakedGood(
        name=data.get('name'),
        price=float(data.get('price')),
        bakery_id=int(data.get('bakery_id'))
    )
    db.session.add(new_baked_good)
    db.session.commit()
    return jsonify(new_baked_good.to_dict()), 201


# ---------------- PATCH ----------------
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    data = request.form

    if 'name' in data:
        bakery.name = data['name']

    db.session.commit()
    return jsonify(bakery.to_dict()), 200


# ---------------- DELETE ----------------
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    db.session.delete(baked_good)
    db.session.commit()
    return jsonify({"message": f"Baked good {id} successfully deleted"}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
