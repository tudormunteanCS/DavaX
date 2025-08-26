#algo.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from math_helpers import pow, fib, factorial_
from db import init_db, get_session
from models import Request

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
init_db()


def persist_request(n, res, endpoint):
    """
    Persist the request to SQLlite database
    :param n: the number from the client
    :param res: the result of the operation
    :param endpoint: the endpoint called
    """
    with get_session() as session:
        req = Request(operation=endpoint, number=n, result=res)
        session.add(req)
        session.commit()


@app.route("/pow")
def hello_world():
    # extract from query parameters n
    n = request.args.get('number', type=int)
    res = pow(n)
    endpoint = "power of two"
    persist_request(n, res, endpoint)
    return jsonify(result=res)


@app.route("/fib")
def fibonacci():
    n = request.args.get('number', type=int)
    res = fib(n)
    endpoint = "fibonacci"
    persist_request(n, res, endpoint)
    return jsonify(result=res)


@app.route("/fact")
def factorial():
    n = request.args.get('number', type=int)
    res = factorial_(n)
    endpoint = "factorial"
    persist_request(n, res, endpoint)
    return jsonify(result=res)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
