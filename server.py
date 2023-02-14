import flask
from flask import Flask, request, jsonify
import psycopg2
from api_logic import predict, get_inputs, conn_string
from flask_cors import CORS
import pandas as pd
import os


# Initialize the app
app = Flask(__name__)
cors = CORS(app)


@app.route("/home")
@app.route("/")
def home():
    return jsonify({'Homepage': 'Healthy and Working!!'})

@app.route('/get_inputs', methods = ['GET'])
def get_names_and_weeks():
    conn = psycopg2.connect(conn_string)
    names_query = """
    SELECT  concat(first_name,' ', second_name)
    FROM elements
    ORDER BY second_name
    """
    rounds_query = """
        select distinct(round) from all_weeks
        where round >= 4
        order by round
    """
    names = pd.read_sql(names_query, con=conn).values.flatten()
    rounds = pd.read_sql(rounds_query, con=conn).values.flatten()+1

    return jsonify(
        {'names': list(names), 'rounds':[str(round_) for round_ in rounds]})



@app.route("/auto_predict", methods=["POST"])
def auto_predict():

    name = request.json['player']
    round_ = request.json['round']

    pred = predict(name=name, round_=round_)
    return jsonify(
        {'predicted': pred})


# For local development:
# app.run(debug=True)

# Heroku will set the port environment variable for
port = os.environ.get("PORT", 5100)
# set debug to false before deployment
app.run(debug=True, host="0.0.0.0", port=port)
