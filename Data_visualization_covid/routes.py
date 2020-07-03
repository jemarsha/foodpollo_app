from flask import render_template, request, jsonify, url_for, redirect
import requests
import pandas as pd
import pickle
import numpy as np
import flask

from Data_visualization_covid import forms

from Data_visualization_covid import app

app.config['SECRET_KEY'] = '7a1159b69cce6d1164ee8332f2559477fa2e059a314e0a9d31d72e40e7329157'

@app.route('/')
@app.route('/index')



def index():
    return render_template('index.html')


@app.route('/recipe_downloader')
def project():
    return render_template('recipe_downloader.html')

@app.route('/project1', methods= ['GET'])
def project1():
    form= forms.UserDem()

    #if form.validate_on_submit():
        #return redirect(url_for('/recipefinder'))
    return render_template('project1.html', title= 'UserDem', form=form)

@app.route('/recipefinder')
def recipe_finder():
    return render_template(('Health_recipe_predictor.html'))


@app.route('/recipefinder', methods=['GET','POST'])
def my_form_post():
    text = request.form['ingredient_text']
    df1 = pd.DataFrame(data=[text], columns=['RECIPE'])
    df1['RECIPE'] = df1['RECIPE'].str.replace('\d+', '')  # strip all digits
    df1['RECIPE'] = df1['RECIPE'].str.replace(' ', '')
    df1['RECIPE'] = df1['RECIPE'].str.replace(',', ' ')
    df1['RECIPE'] = df1['RECIPE'].str.replace('#.', '')
    df1["Count_Of_Strings"] = [len(x.split(' ')) for x in df1['RECIPE']]
    df1["Count_Of_Chars"] = [len(x) for x in df1['RECIPE']]
    # v= TfidfVectorizer()

    v = pickle.load(open("Data_visualization_covid/tfidf.pickle", 'rb'))

    x = v.transform(df1['RECIPE'])

    df2 = pd.DataFrame(x.toarray(), columns=v.get_feature_names())

    df2 = pd.concat([df2, df1], axis=1)
    df2 = df2.drop(columns=['RECIPE'])
    df2 = df2.values
    df2 = df2[:, 1:469]

    df2 = df2.astype('float32')

    model_from_pickle = pickle.load(open("Data_visualization_covid/ingred_model.pickle", "rb"))
    # arr= model_from_pickle.predict(df2).pop()
    arr= 'Healthy' if list(model_from_pickle.predict(df2)).pop() > 0 else 'Unhealthy'
    return render_template('Health_recipe_predictor.html',result= arr)







#@app.route('/predict', methods= ['POST'])

