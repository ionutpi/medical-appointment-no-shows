from flask import Flask, jsonify, json, Response, request, render_template
from flask_cors import CORS
import pandas as pd

from joblib import load
rfo_best = load('no-show-rfo-clf.joblib')
sc = load('no-show-scaler.joblib')

# A very basic API created using Flask that has two possible routes for requests.
# Variables: Age, SMS_received, Days, Previous Missed Appointments, Previous Total Appointments
app = Flask(__name__)
CORS(app)


@app.route('/')
@app.route('/index')
def main_page():
    return render_template("index.html")

@app.route("/calc")
def getPred():

    age  = float(request.args.get('age', None))
    days  = float(request.args.get('days', None))
    pnshap  = float(request.args.get('pnshap', None))
    ptotap  = float(request.args.get('ptotap', None))
    sms  = float(request.args.get('sms', None))
    try:
        ratio = pnshap/ptotap
    except ZeroDivisionError:
        ratio = 0

    X_new = pd.DataFrame(data=[[1, age, 0, 0, 0, 0, 0, sms, days, 0, ptotap, ratio]],
                         columns=['Gender', 'Age', 'Scholarship', 'Hipertension', 'Diabetes',
                                  'Alcoholism', 'Handcap', 'SMS_received', 'DaysToApp', 'AppWeekend',
                                  'PrevAppoint', 'NoShowRatio'])
    X_new_sc = sc.transform(X_new)

    proba = rfo_best.predict_proba(X_new_sc)[0][1]

    flaskResponse = jsonify({'proba': proba})
    #flaskResponse.headers["Content-Type"] = "application/json"

    return flaskResponse

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)