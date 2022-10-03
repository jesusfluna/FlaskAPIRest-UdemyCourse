from flask import Flask, render_template, request, make_response, jsonify

app2 = Flask(__name__)

order = {
    "order1": {
        "size": "small",
        "toppings": "cheese",
        "crust": "thin crust"
    },
    "order2": {
        "size": "big",
        "toppings": "bacon",
        "crust": "rustic"
    },
    "order3": {
        "size": "medium",
        "toppings": "onion",
        "crust": "double"
    },
    "order4": {
        "size": "small",
        "toppings": "chicken",
        "crust": "artisan"
    },
    "order5": {
        "size": "medium",
        "toppings": "ketchup",
        "crust": "light"
    }
}


@app2.route('/')
def index():
    return render_template('index.html')


@app2.route('/orders')
def get_order():
    response = make_response(jsonify(order), 200)
    return response


@app2.route('/orders/<orderid>')
def get_order_details(orderid):
    if orderid in order:
        response = make_response(jsonify(order[orderid]), 200)
        return response
    return "Order no found"


@app2.route('/orders/<orderid>/<items>')
def get_item_details(orderid, items):
    item = order[orderid].get(items)
    if item:
        response = make_response(jsonify(item), 200)
        return response
    return "Order no found"


@app2.route('/orders/<orderid>', methods=["POST"])
def post_order_details(orderid):
    req = request.get_json()
    if orderid in order:
        response = make_response(jsonify({"error": "Order ID already exists"}), 400)
        return response
    order.update({orderid: req})
    response = make_response(jsonify({"message": "Order added to the list"}), 201)
    return response


@app2.route('/orders/<orderid>', methods=["PUT"])
def put_order_details(orderid):
    req = request.get_json()
    if orderid in order:
        order[orderid] = req
        response = make_response(jsonify({"message": "Order updated"}), 200)
        return response
    order[orderid] = req
    response = make_response(jsonify({"message": "Order added to the list"}), 201)
    return response


@app2.route('/orders/<orderid>', methods=["PATCH"])
def patch_order_details(orderid):
    req = request.get_json()
    if orderid in order:
        for k, v in req.items:
            order[orderid][k] = v

        response = make_response(jsonify({"message": "Order updated"}), 200)
        return response

    response = make_response(jsonify({"error": "Order not found"}), 201)
    return response


@app2.route('/orders/<orderid>', methods=["DELETE"])
def delete_order_details(orderid):
    if orderid in order:
        del order[orderid]
        response = make_response(jsonify({"message": "Order deleted"}), 204)
        return response

    response = make_response(jsonify({"error": "Order not found"}), 404)
    return response


if __name__ == '__main__':
    app2.run(debug=True)
