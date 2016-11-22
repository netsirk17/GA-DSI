import Flask
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = flask.Flask(__name__)

df = pd.read_csv('assets/datasets/titanic.csv')
include = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Survived']

# Create dummies and drop NaNs
df['Sex'] = df['Sex'].apply(lambda x: 0 if x == 'male' else 1)
df = df[include].dropna()

X = df[['Pclass', 'Sex', 'Age', 'Fare', 'SibSp']]
y = df['Survived']

PREDICTOR = RandomForestClassifier(n_estimators=100).fit(X, y)

@app.route('/predict', methods=['GET'])
def predict():
	pclass = flask.request.args['Pclass']
    sex = flask.request.args['Sex']
    age = flask.request.args['Age']
    fare = flask.request.args['Fare']
    sibsp = flask.request.args['SibSp']

    item = [pclass, sex, age, fare, sibsp]
    score = PREDICTOR.predict_proba(item)
    results = {'survival chances: ', score[0,1], 'death chances: ', score[0,0]}
    return flask.jsonify(results)

if __name__ == '__main__':
	HOST = '127.01.01'
	PORT = '4000'
	app.run(HOST, PORT)