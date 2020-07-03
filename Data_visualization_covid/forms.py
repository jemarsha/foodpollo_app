from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class UserDem(FlaskForm):
    submit = SubmitField('Sign Up')

    grocery_loc = [0, 1, 2, 3, 4, 5, 6, 7]
    distance_list = [0, 1, 2, 3, 4]
    eat_out_list = [0, 1, 2, 3]
    race_list = [0, 1, 2, 3, 4]
    living_list = [0, 1, 2, 3, 4, 5]

    allergy_list = [0, 1, 2, 3, 4, 5]
    diets_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    sex_list = [0,1,2,3]
    area = [0, 1, 2, 3]

    transportation_list = [0, 1, 2, 3]
    consumption_list = [0, 1, 2, 3,4]

    flavor_list = [0,1,2,3,4,5]

    user_id= StringField('Enter Your Name', validators=[DataRequired(), Length(min=1,max=500)])

    age = StringField('Enter Your Age', validators=[DataRequired(), Length(min=1, max=3)])
    weight_lb = StringField('Enter Your Weight', validators=[DataRequired(), Length(min=1, max=3)])
    height_in = StringField("Enter Your Height in Inches", validators=[DataRequired(), Length(min=1, max=3)])
    groceries = SelectField(
        'Where Do You Buy Groceries? (0=supermarket, 1=superstore,2=farmer_market,3= natural foods store, 4= online grocery, 5= convenience store, 6= Drug Store, 7= Meal Delivery)',
        choices=grocery_loc)

    distance_home_store = SelectField('What is distance to grocery store? 0= 1 mile or less, 1 = 2 miles, 2= 3 miles,3= 4 miles, 4= greater than 4 miles', choices=distance_list)

    transportation = SelectField('What Mode of Transportation do you use? 0= Car, 1= Public Transportation, 2= Walking, 3=Biking', choices=transportation_list)

    health_nutrition_statements = SelectField(
        'How important is it that the food products you purchase are produced in health conscious way? 0= Not at all important, 1= Slightly Important, 2= Moderately Important, 3= Very Important,\
        4= Extremely Important',
        choices=consumption_list)



    tastes = SelectField(
        'What is your favorite flavor? 0= Sweet, 1= Savory, 2= Salty ,3= Spicy, 4= Sour, 5= Bitter',
        choices=flavor_list)

    diet = SelectField('Have You Followed Any Specific Diet? 0=Other, 1= Fasting, 2= Vegan/Vegetarian, 3= Weight Loss Plan, 4= High Protein, 5= Paleo, \
    6= Gluten Free, 7= Cleanse, 8= Low Carb, 9= Ketogenic', choices=diets_list)



    allergies = SelectField('Do you have an allergy? 0=Peanuts, 1= Other Allergies, 2= Dairy, 3= Fish, 4= egg, 5= wheat_gluten', choices=diets_list)

    eat_out_times = SelectField("How many times do you eat out per week? 0= 0-1, 1= 2-4, 2= 5-7, 3= More than 7", choices=eat_out_list)

    race = SelectField("Which of the following best describes your race? 0= Black or African American,  1= White, \
    2= American Indian or Alaska Native, 3= Other, 4= Spanish/Hispanic", choices=race_list)

    living_arrangement = SelectField("Which of the following best describes your living arrangement? 0= Living alone, 1= Living with immediate family, 2= Living with adult children,\
     3=Living with extended family, 4= Living with roommate, 5= Other",
                                     choices=race_list)

    sexuality = SelectField("Do you consider yourself to be: 0= Heterosexual, 1= Gay or Lesbian, 2= Bisexual 3=Other", choices=sex_list)

    living_area = SelectField("Which of the following describes the area you live in? 0= Suburban, 1= Urban, 2=Rural, 3=Small Town", choices=area)



