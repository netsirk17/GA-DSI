import Flask
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = flask.Flask(__name__)
@app.route('/predict', methods=['GET'])

df = pd.read_csv('assets/datasets/titanic.csv')
include = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Survived']

# Create dummies and drop NaNs
df['Sex'] = df['Sex'].apply(lambda x: 0 if x == 'male' else 1)
df = df[include].dropna()

X = df[['Pclass', 'Sex', 'Age', 'Fare', 'SibSp']]
y = df['Survived']

PREDICTOR = RandomForestClassifier(n_estimators=100).fit(X, y)

# @app.route('/predict', methods=['GET'])
def predict():
	pclass = flask.request.args['pclass']
    sex = flask.request.args['sex']
    age = flask.request.args['age']
    fare = flask.request.args['fare']
    sibsp = flask.request.args['sibsp']

    item = [pclass, sex, age, fare, sibsp]
    score = PREDICTOR.predict_proba(item)
    results = {'survival chances': score[0,1], 'death chances': score[0,0]}
    return flask.jsonify(results)


if __name__ == '__main__':
	HOST = '127.01.01'
	PORT = '4000'
	app.run(HOST, PORT)