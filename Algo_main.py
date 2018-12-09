import Rec_nutri as reco
import email_nutri as email
import df_nutri_create as nutri
import product_better as prod_bet
import Product_taken as prod_tak 

def  color_(grade):
	'''Compute color according to the official color of the NutriScore logo'''
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
	'''Compute NutriScore and recomendation to send to the app and by email '''

	# Remove product with 0 as quantity
	list_prod = [prod_quant for prod_quant in dict_prod['Product'] if prod_quant[1] != 0]
	list_Api = [prod_quant for prod_quant in dict_prod['API'] if prod_quant[1] != 0]

	# Compute NutriScore and usefull number for the recomendation
	dict_nutri = nutri.main_nutri(list_prod, df, list_Api)

	# Text for the app
	if dict_nutri['NutriScore_Beverages'] != None:
		Nutri_beve_text = 'Nutri-Score for your beverages : {} (with a total score of {})'\
		.format(dict_nutri['NutriScore_Beverages'].upper(), dict_nutri['Score_Beverages'])
	else:
		Nutri_beve_text = 'Nutri-Score for your beverages : -'

	if dict_nutri['NutriScore_Non_Beverages'] != None:
		Nutri_food_text = 'Nutri-Score for your food : {} (with a total score of {})'\
		.format(dict_nutri['NutriScore_Non_Beverages'].upper(), dict_nutri['Score_Non_Beverages'])
	else:
		Nutri_food_text = 'Nutri-Score for your food : -'

	# if the user ask for recomendation
	if dict_set['Rec']:

		# text about defiencies, excess, ...
		text_rec = reco.Rec_text(dict_set['Sex'], dict_set['Age'], dict_set['Pal'], dict_set['Day'], dict_set['Weight'], dict_nutri)
		
		# text about healthier product
		text_healthier_prod = prod_bet.Better_product_rec(dict_prod['Product'], df)
		
		# text about all the product selected
		text_prod = prod_tak.product_list(list_prod, df, list_Api)

		text_head = '''<head><h1 style="color:#193086">Expanding Nutri-Score  : take your menu to the next level</h1>
		<h3 style="color:white">ADA 2018 - by NutriTeam</h3></head>'''

		text_welcome = '''<p>Hi <b>{} {}</b>,\n Here your report : </p>'''.format(dict_set['Name'], dict_set['Surname'])

		text_nutri = '''<h2 style="color:#3C627E">Nutri-Score</h2>
		<p style="color:{}">{}</p>
		<p style="color:{}">{}</p>'''.format(color_(dict_nutri['NutriScore_Beverages']), Nutri_beve_text, \
		color_(dict_nutri['NutriScore_Non_Beverages']), Nutri_food_text)

		text_end = '''<footer><h4>Thanks for using our app ! <a href="https://nutriteam.github.io/Nutri_Score/home">
		Please visit our website</a>\n</h4><br>If you see mistakes or missing products, go to <a href="https://world.openfoodfacts.org/"
		target = "_blanck">Open Food Facts</a> to correct or add products. Improve with us the database !<br><h5> - by NutriTeam</h5></footer>'''

		text = text_head + text_welcome + text_nutri + text_rec + text_healthier_prod + text_prod + text_end
		# send email
		email.Send_rec(dict_set['Email'], text)

	return (Nutri_beve_text,  Nutri_food_text)



