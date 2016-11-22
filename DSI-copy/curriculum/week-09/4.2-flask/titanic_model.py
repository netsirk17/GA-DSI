import numpy as np
import pandas as pd
import pickle

from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import accuracy_score
#from sklearn.cross_validation import cross_val_score, cross_val_predict

import flask
app = flask.Flask(__name__)



filepath = '/users/kristensu/dropbox/ga-dsi/dsi-copy/projects/projects-weekly/project-05/titanic_model_df.pkl'

with open(filepath, 'r') as picklefile:
	p = pickle.load(picklefile)

model_cols = ['sex', 'sibsp_norm', \
			'port_C', 'port_Q', 'port_S', \
            'pclass_1.0', 'pclass_2.0', 'pclass_3.0', \
            'bin_child', 'bin_adult', 'bin_elderly']

X = p.loc[:, model_cols]
y = p['survived']

model = LogisticRegressionCV()
fitmodel = model.fit(X,y)

@app.route('/titanic_form', methods = ['GET'])
def form():
	with open('titanic_form.html') as viz_file:
		return viz_file.read()


@app.route('/predictions', methods = ['POST', 'GET'])
def predictions():
	if flask.request.method == 'POST':
		inputs = flask.request.form
		sex = inputs['sex'][0]
		sibsp_norm = inputs['sibsp_norm'][0]
		port_C = inputs['port_C'][0]
		port_Q = inputs['port_Q'][0]
		port_S = inputs['port_S'][0]
		pclass_1 = inputs['pclass_1'][0]
		pclass_2 = inputs['pclass_2'][0]
		pclass_3 = inputs['pclass_3'][0]
		bin_child = inputs['bin_child'][0]
		bin_adult = inputs['bin_adult'][0]
		bin_elderly = inputs['bin_elderly'][0]

		features = [sex, sibsp_norm, port_C, \
					port_Q, port_S, pclass_1, \
					pclass_2, pclass_3, bin_child, \
					bin_adult, bin_elderly]
		probability = fitmodel.predict_proba(features)
		#score = fitmodel.accuracy_score(features) 
		results = {'Survival chances: ': probability[0][1],
					'Certain death chances: ': probability[0][0]}

		return flask.jsonify(results)

if __name__ == '__main__':
	HOST = '127.0.0.1'
	PORT = '4000'
	app.run(HOST, PORT)



