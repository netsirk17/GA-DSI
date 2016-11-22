import flask
app = flask.Flask(__name__)


import numpy as numpy
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('assets/datasets/titanic.csv')
include = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Survived']

df['Sex'] = df['Sex'].apply(lambda x: 0 if x == 'male' else 1)
df = df[include].dropna()

X = df.drop(['Survived'], axis = 1)
y = df['Survived']

PREDICTOR = RandomForestClassifier(n_estimators=100).fit(X,y)

#--ROUTES--#
@app.route('/page', methods=["GET"])
def page():
    with open('page.html') as viz_file:
        return viz_file.read()

@app.route('/result', methods=[ 'POST', 'GET'])
def result():
    if flask.request.method == 'POST':
        inputs = flask.request.form
        pclass = inputs['pclass'][0]
        sex = inputs['sex'][0]
        age = inputs['age'][0]
        fare = inputs['fare'][0]
        sibsp = inputs['sibsp'][0]

        item = [pclass, sex, age, fare, sibsp]
        score = PREDICTOR.predict_proba(item)
        results = {'survival chances: ': score[0,1], 'death chances': score[0,0]}
        return flask.jsonify(results)

# @app.route('/predict', methods=["GET"])
# def predict():
#     pclass = flask.request.args['pclass']
#     sex = flask.request.args['sex']
#     age = flask.request.args['age']
#     fare = flask.request.args['fare']
#     sibsp = flask.request.args['sibsp']

#     item = [pclass, sex, age, fare, sibsp]
#     score = PREDICTOR.predict_proba(item)
#     results = {'survival chances: ': score[0,1], 'death chances': score[0,0]}
#     return flask.jsonify(results)



if __name__ == '__main__':

    HOST = '127.0.0.1'
    PORT = '3000'
    app.run(HOST, PORT)