import flask
from flask import request
from numpy import round_
from fpl_api import manual_prediction, auto_prediction, get_inputs, feature_names

# Initialize the app
app = flask.Flask(__name__)


@app.route("/")
def home():
    return flask.render_template('main_page.html')


@app.route("/manual-predict", methods=["POST", "GET"])
def predict():
    x_input, predicted = manual_prediction(request.args)
    return flask.render_template('predictor.html', x_input=x_input,
                                 feature_names=feature_names,
                                 predicted=predicted)


@app.route("/auto-predict", methods=["POST", "GET"])
def auto():

    full_name = request.args.get('full_name')
    round_ = request.args.get('round_')

    all_full_names, all_round = get_inputs()
    print(all_full_names)
    answer = auto_prediction(full_name=full_name, round_=round_)
    return flask.render_template('auto.html',
                                 answer=answer,

                                 all_full_names=all_full_names,
                                 all_round=all_round)


# For local development:
app.run(debug=True)