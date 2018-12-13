# Imports
import Rec_nutri as reco
import email_nutri as email
import df_nutri_create as nutri
import product_better as prod_bet
import Product_taken as prod_tak 

def  color_(grade):
	'''Compute colors according to the official colors of the NutriScore logo. '''
	'''
		Input :
		grade(str): official grade from 'a' (best) to 'e' (worst)

		Output :
		(str): HEX color code
	'''

	# The HEX color corresponding to the grade is returned
	if grade == 'a':
		return '#008141'
	elif grade == 'b':
		return '#85BB2F'
	elif grade == 'c':
		return '#FECB02'
	elif grade == 'd':
		return '#EE8102'
	elif grade == 'e':
		return '#E63E11'
	else:
		return '#990406'

def algo(dict_prod, dict_set, df):
	'''Compute NutriScore and recommendation to send to the app and by email. '''
	'''
		Input :
		dict_prod(dictionary): contains the products consumed by the user
		dict_set(dictionary): contains the settings/profile information
		df(pandas dataframe): complete dataframe of the products

		Output :
		(tuple(str,str)): text of the recommendation
	'''

	# Product with 0 as quantity are removed
	list_prod = [prod_quant for prod_quant in dict_prod['Product'] if prod_quant[1] != 0]
	list_Api = [prod_quant for prod_quant in dict_prod['API'] if prod_quant[1] != 0]

	# Compute NutriScore and all other useful values for the recommendation
	dict_nutri = nutri.main_nutri(list_prod, df, list_Api)

	# Text for the app
	if dict_nutri['NutriScore_Beverages'] != None:
		Nutri_beve_text = 'NutriScore for your beverages : {} (with a total score of {})'\
		.format(dict_nutri['NutriScore_Beverages'].upper(), dict_nutri['Score_Beverages'])

	else:
		Nutri_beve_text = 'Nutri-Score for your beverages : -'

	if dict_nutri['NutriScore_Non_Beverages'] != None:
		Nutri_food_text = 'NutriScore for your food : {} (with a total score of {})'\
		.format(dict_nutri['NutriScore_Non_Beverages'].upper(), dict_nutri['Score_Non_Beverages'])

	else:
		Nutri_food_text = 'NutriScore for your food : –'

	# If the user asked for a recommandation (sent by email)
	if dict_set['Rec']:

		# Text about defiencies, excess, ...
		text_rec = reco.Rec_text(dict_set['Sex'], dict_set['Age'], dict_set['Pal'], dict_set['Day'], dict_set['Weight'], dict_nutri)
		
		# Text for recommendation  of healthier products
		text_healthier_prod = prod_bet.Better_product_rec(dict_prod['Product'], df)
		
		# Text recap about selected product 
		text_prod = prod_tak.product_list(list_prod, df, list_Api)

		# Title text
		text_head = '''<head><h1 style="color:#193086">Expanding Nutri-Score : take your menu to the next level</h1>
		<h3 style="color:white">ADA 2018 - by NutriTeam</h3></head>'''

		# Header text
		text_welcome = '''<p>Hi <b>{} {}</b>,\n here is your report : </p>'''.format(dict_set['Name'], dict_set['Surname'])

		# Call color_ function to get the color of the text
		text_nutri = '''<h2 style="color:#3C627E">Nutri-Score</h2>
		<p style="color:{}">{}</p>
		<p style="color:{}">{}</p>'''.format(color_(dict_nutri['NutriScore_Beverages']), Nutri_beve_text, \
		color_(dict_nutri['NutriScore_Non_Beverages']), Nutri_food_text)

		# End text
		text_end = '''<footer><h4>Thanks for using our app ! <a href="https://nutriteam.github.io/Nutri_Score/home">
		Please visit our website</a>\n</h4><br>If you find missing or erroneous products, we invite you to go to <a href="https://world.openfoodfacts.org/"
		target = "_blanck">Open Food Facts</a> to add or edit the product pages. Improve with us the database !<br><h5> - by NutriTeam</h5></footer>'''

		# Concatenation of all texts
		text = text_head + text_welcome + text_nutri + text_rec + text_healthier_prod + text_prod + text_end
		
		# Send email
		email.Send_rec(dict_set['Email'], text)

	# Call color_ function to get the color of the text and print global scores (on app)
	Nutri_beve_text_app = '[color={}]{}[/color]'.format(color_(dict_nutri['NutriScore_Beverages'])[1:], Nutri_beve_text)
	Nutri_food_text_app = '[color={}]{}[/color]'.format(color_(dict_nutri['NutriScore_Non_Beverages'])[1:], Nutri_food_text)

	# Return texts
	return (Nutri_beve_text_app,  Nutri_food_text_app)



