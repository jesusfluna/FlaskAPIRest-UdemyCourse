from flask import Flask, render_template, request, make_response, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Myapp(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(500))
    toppings = db.Column(db.String(500))
    crust = db.Column(db.String(500))


class MyAppSchema(ma.Schema):
    class Meta:
        fields = ('order_id', 'size', 'toppings', 'crust')


my_app_schema = MyAppSchema(many=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/orders')
def get_orders():
    entries = Myapp.query.all()
    result = my_app_schema.dump(entries)
    return jsonify(result)


@app.route('/orders', methods=["POST"])
def post_orders():
    req = request.get_json()
    order_id = req['order_id']
    size = req['size']
    toppings = req['toppings']
    crust = req['crust']

    new_entry = Myapp(order_id=order_id, size=size, toppings=toppings, crust=crust)

    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for("get_orders"))


@app.route('/orders/<order_id>', methods=["DELETE"])
def post_orders(order_id):
    entry = Myapp.query.get_or_404(order_id)

    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for("get_orders"))


@app.route('/orders/<order_id>', methods=["PUT"])
def put_orders(order_id):
    req = request.get_json()
    entry = Myapp.query.get(order_id)

    entry.size = req['size']
    entry.toppings = req['toppings']
    entry.crust = req['crust']

    db.session.add(entry)
    db.session.commit()

    return redirect(url_for("get_orders"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
