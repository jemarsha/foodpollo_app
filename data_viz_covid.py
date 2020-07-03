import numpy as np
import pandas as pd
import turicreate as tc
from flask import make_response
from flask import render_template, request


from Data_visualization_covid import AllRecipes
from Data_visualization_covid import app
from Data_visualization_covid.forms import UserDem
import random
import re

vals = {'enjoy_chinese':['Abalone Meuniere Mandarin'
'Aged Tofu (Figi)',
'Al and Tipper Gore’s Chinese Chicken with Walnuts',
'Almond Creme',
'Almond Tea Jelly',
'Anise Molasses Brisket Braised in a Wok',
'Asian Black Bean Sauce',
'Asian Cabbage Stir Fry',
'Asian Hot-Que Grill Sauce For Chicken, Beef Or Pork',
'Asian Marinated Eggplant',
'Asian Pear and Lyche Strudel',
'Asparagus And Chicken In Black Bean Sauce',
'Asparagus and Mushrooms with Black Bean Sauce'],
      'enjoy_british': ['Bacon Supper Snack',
'Baked Flounder (English)',
'Baked Gammon in Cider (English)',
'Bangers or Oxford Sausages',
'Basic Bangers',
'Bentons’s Sauce - A Variation On The Traditio',
'Black Pudding From Scratch (English)'],

      'enjoy_cajun': ['Acadian Peppered Shrimp', 'A.C.’s Potato Rolls',
'All Purpose Marinade', 'Alligator Cacciatora Banquet', 'Alligator Grand Chenier'
        'Alligator Jambalaya','crawfish-jambalaya2', 'blacked-spice-fish1', 'crab-cocktail1', 'praline-sauce1',
                      'shrimp-salad1', 'potato-salad2', 'jambalaya1', 'liver-rice1', 'vegetable-salad1'],


      'enjoy_canadian': ['Aloo Ko Achar (Potato Salad)', 'Apple Pancakes From the Townships',
'Apple Pork Chops', 'Baked Cod with Stuffing', 'Baked Peameal Bacon','apple-dumplings1', 'skewered-mozzarella-bacon1', 'pumpkin-potatoes1',
                         'pb-nanaimo-bars1', 'cheese-soup1', 'provolone-mushroom-sandwiches1'],
      'enjoy_caribbean': ['Ackee Soup', 'Ajiaco', 'Arroz Con Pollo (Chicken With Yellow Rice)','Asopao De Pollo'
'Bacalao A La Vizcaina Codfish Fricassee','salad-platter1', 'cuban-chicken1', 'empanadillas1',
                          'okra-salad1', 'jamaican-rice-peas1', 'vegetable-stew1'],
      'enjoy_french': ['A Croque Monsieur Salad', 'Asparagus Vinaigrette'
'Beignes Aux Dattes De Ma Mere', 'Beinets Or French Fritters'
'Bitoque Provencal','snails-menetrel1', 'cabbage-salad1', 'pot-au-feu1', 'ragout-pattes1', 'chocolate-mousse1',
                       'chicken-winter-vegetables1', 'feuillete-descargots1', 'paris-brest1'],
      'enjoy_german': ['frankfurt Green Sau','Bean Soup with Frankfurter','Fred’s German Potato Dumplings',
'Fresh Asparagus', 'Stuffed Cabbage Rolls','labskaus1', 'erbsenpuree1', 'boiled-pork1', 'holderkuechle1', 'ropfkrapfen1', 'hot-noodle-salad1', 'stollen1', 'weihnachtsgans1', 'stollen2', 'orangenplaetzchen1'],
      'enjoy_greek': ['Anginares Tarama','Another Gyros','Apple Baklava','Peas Latheros','diabetic-gyros1', 'soureki1', 'garithes-yiouvetsi1', 'spanakopita6', 'dolmas1', 'avgolemono01',
                      'spanikopita1', 'boned-oysters1', 'chopped-meat-stuffing1','labskaus1', 'erbsenpuree1', 'boiled-pork1', 'holderkuechle1', 'ropfkrapfen1', 'hot-noodle-salad1', 'stollen1', 'weihnachtsgans1', 'stollen2', 'orangenplaetzchen1'],
      'enjoy_indian': ['Hoppers','Spiced Green-Pea Puree','vegetable stew','Avocado Kashmir',
                       'Penjabi Style Eggplant','omelette-pakaki-curry', 'bread-dosa1', 'vegetable-biriyani1', 'kashmiri-rogan-josh1', 'mixed-vegetable-curry1', 'chicken-tandoori1', 'omelette-pakaki-curry1', 'lassi',
                       'sherba', 'andoori-chicken1', 'marak-perot-kar1', 'mint-coriander-dip1', 'pumpkin-soup1'],

      'enjoy_italian': ['zuccotto Ripieno','Andrea’s Baked Ziti','Angel Hair With Balsamic Tomatoes',
                        'risotto-four-cheeses1', 'polenta-beef-sausage-stew1', 'zucchini-lamb-mint1', 'squid-spaghetti1', 'crusty-fettucine1', 'asparagus-prosciutto-bundles1', 'poached-oranges1', 'pasta-balsamic-tomatoes1', 'raisin-bread1', 'risotto-con-calamari1', 'sausage-cacciatore1', 'pane-giallo1', 'risotto-wild-mushrooms1',
                        'baked-zucchini1', 'fettucine-alfredo1', 'risotto-crabmeat-basil1'],

      'enjoy_japanese': ['cold Marinated Asparagus', 'Baked Ziti and Vegetables','Baked Ziti With Ricotta Cheese','kuri-gohan', 'sukiyaki', 'horensho-hitashi1', 'gyoza1', 'monkfish-ginger-sauce1', 'shrimp-cucumber-salad1'],
      'enjoy_mexican': ['Cochiti Green Chile Stew', 'Cod With Garlic', 'Corn Fritters','Corn Meal Dough','miniature-frittatas1', 'nuevo-frijoles1', 'exmex-enchiladas1',
                        'chicken-corn-chowder1', 'chile-pablano1', 'chicken-beef-fajitas1', 'chicken-acapulco1', 'flour-tortillas1', 'chalupas1', 'red-pepper-quesadilla1', 'salmon-quesadillas1'],
      'enjoy_thai': ['Cochiti Green Chile Stew', 'Cod With Garlic','Corn Fritters','Corn Meal Dough','Thai Chicken Salad with Collard Greens','yam-wunsen-sai-mu1',
                     'stir-fried-beef-mint1', 'figgy-chicken-salad1', 'kaeng-khua-saparot1', 'squid-salad1',
                     'pork-basil1', 'fried-noodles1', 'greens-oyster1', 'fried-noodles2', 'kaeng-ped-cai1', 'marinated-beef1',
                     'fried-corn-cakes1', 'bean-thread-salad1', 'chicken-curry1', 'fried-noodles3', 'mee-krob2', 'som-tam1', 'glass-noodles1', 'pad6', 'special-chicken-chillies1',
                     'pad7', 'mini-spring-rolls1', 'prik-kaeng-kiao-wan1', 'mee-krob3',
                     'asparagus-mushrooms1', 'ea1', 'kai-tam1', 'neua-pad-kimao1',
                     'charcoaled-squid--pla-muk-yang1', 'drunkards-noodles1']}



#print(vals['enjoy_british'])
#print(vals.keys())

def convert_to_num(name):
    count_sum = 0
    for letter in name:
        count_sum += ord(letter)

    return count_sum


@app.route('/index', methods=['GET'])
@app.route('/project1', methods=['GET', 'POST'])
def main():
    # df = read_data()
    # df_side_info = create_side_info(df)
    # df_side_info = categorize_column(df_side_info, ['race', 'diet', 'allergy', 'groceries'])
    # df_turi, df_side_info = to_recommendation_format(df, df_side_info)
    # df_turi = df_turi.loc[df_turi['rating'] != -2][0:20]
    recommendations= []
    form = UserDem()

    input_dict = {}
    if form.is_submitted():  # form.validate_on_submit():

        for field in form:

            input_dict[field.name] = [field.data]

        # flash(f'Account created for {form.Age.data}!', 'success')

        #aging = form.Age.data
        #grocery = form.Groceries.data
        input_dict.pop('submit')
        input_dict.pop('csrf_token')
        #name= input_dict.pop('user_id')
        # return redirect(url_for('project1'))
    input_dict['user_id'][0] = convert_to_num(input_dict['user_id'][0])
    name= input_dict['user_id'][0]
    new_user_info= tc.SFrame(input_dict)
    print(new_user_info)
    #name= input_dict.pop('user_id')[0]
    # rating = request.form.get("ratings", None)
    # grocery= request.form.get("glist", None)
    loaded_model = tc.load_model('Foodpollo_Recommender')
    df_turi= loaded_model.recommend([name], new_user_data=new_user_info)
    df_turi = df_turi.to_dataframe()
    df_turi= df_turi[['item_id', 'rank']].head(10)

    for i in range(df_turi.shape[0]):

        if df_turi.iloc[i, 0] in vals:
            extracted_name = re.sub('enjoy_', "", df_turi.iloc[i, 0])

            extracted_name += ' recipes'

            # print('Your recommended meals for {} are \n {} \n'.format(extracted_name,random.sample(vals[df_turi.iloc[i,0]],2)))
            recommendations.append('Your recommended meals for {} are {}'.format(extracted_name,
                                                                   random.sample(vals[df_turi.iloc[i, 0]], 2)))

    #return render_template('project1.html', movie_names=[df_turi.to_html(classes='data')], titles=df_turi.columns.values, form=form)
    return render_template('project1.html', recommendations=recommendations, form=form)
    # movie_names=df_turi)
    #return render_template('project1.html', need_dict=df_turi.head(10), form=form)
    # movie_names=df_turi)


"""
Outputs name, ingredients, directions, cooking time, ratings, and nutrients to file
"""


@app.route('/recipe_downloader', methods=['GET', 'POST'])
def recipe_crawler():
    text = request.form['recipe_input']
    query_options = {
        "wt": str(text),  # "pork curry",  # Query keywords
        "ingIncl": "olives",  # 'Must be included' ingrdients (optional)
        "ingExcl": "onions salad",  # 'Must not be included' ingredients (optional)
        "sort": "re"  # Sorting options : 're' for relevance, 'ra' for rating, 'p' for popular (optional)
    }
    query_result = AllRecipes.search(query_options)

    # Just need to loop through the recipes and add them to a csv that downloads
    # print(query_result[0:5])

    recipe_urls = []

    for i in range(len(query_result)):
        recipe_urls.append(query_result[i]['url'])
    # main_recipe_url = query_result[0]['url']

    detailed_recipe = AllRecipes.get(recipe_urls[0])
    for url in recipe_urls[1:10]:
        # for i in range(5):

        # detailed_recipe.loc[i] = AllRecipes.get(recipe_urls[i])
        pimp = AllRecipes.get(url)
        # print(pimp)
        detailed_recipe = pd.concat([detailed_recipe, pimp])
    # print(detailed_recipe)

    # hold = []
    # for ingredient in detailed_recipe['ingredients']:
    #    hold.append(ingredient)
    resp = make_response(detailed_recipe.to_csv(index=False))
    resp.headers["Content-Disposition"] = "attachment; filename= {}.csv".format(text)
    resp.headers["Content-Type"] = "text/csv"
    return resp
    # return render_template('recipe_downloader.html', names= resp) #names=[detailed_recipe.to_html(classes='data')],titles=detailed_recipe.columns.values)


if __name__ == '__main__':
    app.run(debug=True)

# app.run(host='0.0.0.0', port=3001, debug=True)
