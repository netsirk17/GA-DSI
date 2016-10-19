import jinja2
import os
from flask import Flask, render_template, request, jsonify
from flask.ext.cors import CORS, cross_origin
import pandas as pd
import numpy as np
import pickle
from math import log
from sklearn.ensemble import GradientBoostingClassifier
from lifelines import AalenAdditiveFitter


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# with open('aaf_99_200.pkl', 'r') as picklefile:
#     aaf = pickle.load(picklefile)

df = pd.read_csv("data/obs.csv")
df.drop("Unnamed: 0", axis=1, inplace=True)
x_class = df.drop(["time_class","shelter_time"], axis=1)
y_class = df["time_class"]

model= GradientBoostingClassifier(n_estimators=50,max_features=0.2,min_samples_split=5,subsample=1,max_depth=10,min_samples_leaf=5)
model.fit(x_class, y_class)

word_df = pd.read_csv("data/words.csv")
word_df.drop("Unnamed: 0", axis=1, inplace=True)
word_list= list(word_df["word"].values)

names_df = pd.read_csv("data/names.csv")
names_df.drop("Unnamed: 0", axis=1, inplace=True)
all_names= list(names_df["human_name"].values)

adopt_sub1 = df.drop("time_class", axis=1)
# adopt_sub1.sample(frac=0.5)

aaf_99_200 = AalenAdditiveFitter(alpha=0.99, coef_penalizer=200.0, fit_intercept=True)
aaf_99_200.fit(adopt_sub1, 'shelter_time')

@app.route('/')
@cross_origin()
def home_page():
    return render_template('index.html')

@app.route('/result', methods=['GET'])
@cross_origin()
def predict():

    try:
        age = int(request.args['age'])
    except:
        age = 3
    try:
        dog_name = str(request.args['dog_name'])
        if dog_name == "":
            dog_name = "dog's name"
    except:
        dog_name = "dog's name"
    try:
        in_sex = int(request.args['sex'])
    except:
        in_sex = 0
    try:
        in_neuter = int(request.args['neuter'])
    except:
        in_neuter = 0
    try:
        colour = str(request.args['colour'])
        if colour == "":
            colour = "light"
    except:
        colour = "light"
    try:
        mix = int(request.args['mix'])
    except:
        mix = 0
    breed1 = str(request.args['breed1'])
    if breed1 == "":
        breed1 = "other"
    breed2 = str(request.args['breed2'])
    if breed2 == "":
        breed2 = "nobreed"
    intake = str(request.args['intake'])
    if intake == "":
        intake = "Stray"
    condition = str(request.args['condition'])
    if condition == "":
        condition = "Normal"
    try:
        month = int(request.args['month'])
    except:
        month = 1
    try:
        total_number_dogs = int(request.args['total_number_dogs'])
    except:
        total_number_dogs= 1

# create dictionary for array
    predict_vars = ['age_log', u'total_number_dogs', 'size', 'coat', 'word_name', u'in_sex', 'dark mix', 'in_neuter', \
    'energy', 'cute_name', 'groom', 'Normal', 'Stray', 'light mix', 'popular_shelter_name', 'human_name', \
    'Owner Surrender', 4, 'popular_dog_name', 'sporting', 'herding', 'toy', 'light', 6, 'other', 3, \
    'Public Assist', 11, 'chihuahua', 'aggressive']


#initialize empty df for predictions
    pred_df = pd.DataFrame(columns=predict_vars)
    pred_df.loc[1,:]=0
# calculate name related features
    name = dog_name.lower()

    top_dog_names = [u'cookie', u'blue', u'daisy', u'bella', u'rocky', u'jackson', u'king', u'duke', u'roscoe',
                     u'lucy', u'chico', u'fiona', u'princess', u'lola', u'monty', u'morgan', u'bailey', u'molly',
                     u'luke', u'jack', u'raven', u'max', u'junior', u'sadie', u'reese', u'libby', u'oreo', u'oliver',
                     u'honey', u'brownie', u'wally', u'rusty', u'tulip', u'cane', u'hercules', u'lady', u'diesel',
                     u'maggie', u'izzy', u'colt', u'earl', u'penny', u'murphy', u'bentley', u'lulu', u'sky', u'zoey',
                     u'cooper', u'jazz', u'caleb', u'snowy', u'ellie', u'lily', u'star', u'rosie', u'goldie']
    top_dog_names_shelter = ['bella', 'max', 'daisy', 'charlie', 'rocky', 'princess', 'buddy', 'lucy', 'lucky', 'luna',
                             'coco', 'chico', 'lola', 'sadie', 'jack', 'lady', 'blue', 'molly', 'duke', 'toby', 'bear',
                             'diamond', 'sasha', 'shadow', 'chloe', 'rosie', 'brownie', 'zeus', 'oso', 'lily', 'ginger',
                             'rex', 'marley', 'oreo', 'king', 'cookie', 'buster', 'maggie', 'ruby', 'roxy']

    pred_df["age_log"] = log(age)
    pred_df["total_number_dogs"] = total_number_dogs
    pred_df["in_sex"] = in_sex
    pred_df["in_neuter"] = in_neuter

    if colour in predict_vars:
        pred_df[colour] = 1
    if month in predict_vars:
        pred_df[month] = 1
    if condition in predict_vars:
        pred_df[condition] = 1
    if intake in predict_vars:
        pred_df[intake] = 1

    breed_list = [breed1.lower(), breed2.lower()]
    breed_list = [i for i in breed_list if i!="nobreed"]
    for i in breed_list:
        if i in predict_vars and i != "other":
            pred_df[i] = 1
    akc = pd.read_csv("data/akc.csv")
    akc["breed"] = akc["breed"].apply(lambda x: x.lower())
    akc.set_index("breed", inplace=True)

    aggressive  = ["pit bull","american staffordshire terrier","staffordshire bull terrier"]
    energy_list = []
    size_list = []
    coat_list = []
    groom_list = []

    ave_energy = 2.4
    ave_size = 1.75
    ave_coat = 1.35
    ave_groom = 1.15

    all_breeds = akc.index.values

    for i in breed_list:
        if i in all_breeds:
            energy_list.append(akc.loc[i,"energy"])
            size_list.append(akc.loc[i,"size"])
            coat_list.append(akc.loc[i,"coat"])
            groom_list.append(akc.loc[i,"groom"])
            if i in aggressive:
                pred_df["aggressive"]=1
            if pd.isnull(akc.loc[i,"group"]):
                pred_df["other"] = 1
            else:
                if akc.loc[i,"group"] in predict_vars:
                    pred_df[akc.loc[i,"group"]] = 1
        else:
            energy_list.append(ave_energy)
            size_list.append(ave_size)
            coat_list.append(ave_coat)
            groom_list.append(ave_groom)

    pred_df["energy"] = np.mean(energy_list)
    pred_df["size"] = np.mean(size_list)
    pred_df["coat"] = np.mean(coat_list)
    pred_df["groom"] = np.mean(groom_list)

    if name in all_names:
        pred_df["human_name"]=1

    if name in top_dog_names:
        pred_df["popular_dog_name"]=1

    if name in top_dog_names_shelter:
        pred_df["popular_shelter_name"]=1

    def cute_name(x):
        try:
            if x[-2:] =="ee" or x[-2:] =="ie" or x[-2:] =="ey" or x[-1]=="y"or x[-1]=="i":
                return 1
            else:
                return 0
        except:
            return 0
    pred_df["cute_name"] = cute_name(name)

    if name in word_list:
        pred_df["word_name"] = 1

# predict outcome binary
    pred_array = np.array(pred_df)

    scores = model.predict_proba(pred_array)
    if scores[0][1] >=0.60:
        prediction = 1
    else:
        prediction = 0
    if prediction ==1:
        pred_string = "This dog is likely to be adopted within 8 days."
    else:
        pred_string = "This dog is likely to take longer than 8 days to be adopted."

    pred_df = pred_df.applymap(lambda x: float(pd.to_numeric(x)))
    surv = aaf_99_200.predict_survival_function(np.array(pred_df)).iloc[:101,:]
    selector = range(0,100,5)
    surv = surv.loc[selector,:]
    labels = [str(i) for i in selector]
    vals = [round(i,2) for i in surv.values]

    grp_vals = [0.99, 0.66, 0.43, 0.33, 0.27, 0.22, 0.19, 0.16, 0.14, 0.12, 0.1, 0.09, 0.07, 0.06, 0.05, 0.03, 0.03, 0.02, 0.02, 0.01]


    # calc = [str(age), dog_name, str(in_sex), str(in_neuter), colour, str(mix), breed1, breed2, intake, condition, str(month), str(total_number_dogs)]
    values = [age, 2*age, 3*age]
    results = {"prediction":pred_string, "dog_name":dog_name, "labels":labels, "values": vals, "grp_values": grp_vals}

    return jsonify(results)

if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)
