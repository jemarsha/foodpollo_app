from Data_visualization_covid import AllRecipes
from flask import render_template, request, jsonify
from Data_visualization_covid import app

import pandas as pd
import csv
import numpy as np
from sklearn.cluster import KMeans
import flask
from Data_visualization_covid import routes


"""
Outputs name, ingredients, directions, cooking time, ratings, and nutrients to file
"""
@app.route('/recipe_downloader', methods=['GET','POST'])
def recipe_crawler(text):
    text= request.form['recipe_input']
    query_options = {
        "wt": str(text), #"pork curry",  # Query keywords
        #"ingIncl": "olives",  # 'Must be included' ingrdients (optional)
        #"ingExcl": "onions salad",  # 'Must not be included' ingredients (optional)
        "sort": "re"  # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
    }
    query_result = AllRecipes.search(query_options)

    # Just need to loop through the recipes and add them to a csv that downloads
    # print(query_result[0:5])
    main_recipe_url = query_result

    detailed_recipe = AllRecipes.get(
        main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)
    #print(detailed_recipe['nutrients'])
    return render_template('recipe_downloader.html', names= detailed_recipe['nutrients'])


if __name__== '__main__':
    recipe_crawler(request.form['recipe_input'])