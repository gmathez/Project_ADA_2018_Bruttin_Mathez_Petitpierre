import pandas as pd
import computeNutriScore as nutri_sc
from API_US_agri import fill_from_Api

def create_dataframe(list_product, data_food):
	'''Create a dataframe that contains all the product selected by the user '''

	column_for_data_food = ['product_name','categories_tags','energy_100g','fat_100g',
                        'saturated-fat_100g','sugars_100g','salt_100g','sodium_100g',
                        'fruits-vegetables-nuts_100g','fruits-vegetables-nuts-estimate_100g',
                        'fiber_100g','proteins_100g', 'quantites']
	df_product = pd.DataFrame(columns = column_for_data_food)

	for barcode, quantites in list_product:
		df_product = df_product.append(data_food.loc[barcode])
		df_product.loc[barcode, 'quantites'] = quantites
	return df_product[column_for_data_food]

def multpliply_quantites(df_product):
	for index in range(len(df_product)):
		quantites = df_product.iat[index, 12]
		for column in range(2, len(df_product.columns)):
			if (df_product.columns[column] != 'quantites'):
				df_product.iat[index, column] = df_product.iat[index, column]  * quantites / 100
	return df_product


def sum_dataframe(df_product):
	df_product_copy = df_product.copy()
	sum_ = df_product_copy.sum()
	return pd.DataFrame(sum_.values, index = sum_.index).T


def separate_dataframe(df_product):
	'''Separate beverages and non-beverages product '''
	df_beverages = df_product[df_product.categories_tags.str.contains('beverages', case=False) &\
        ~df_product.categories_tags.str.contains('en:plant-based-foods,', case=False) &\
        (~ df_product.categories_tags.str.contains('milk', case=False))].copy()

	df_non_beverages = df_product[~(df_product.categories_tags.str.contains('beverages', case=False) &\
        ~df_product.categories_tags.str.contains('en:plant-based-foods,', case=False) &\
        (~ df_product.categories_tags.str.contains('milk', case=False)))].copy()
	return df_beverages, df_non_beverages

def separate_water(df_beverages):
	df_water = df_beverages[df_beverages.categories_tags.str.contains('en:spring-waters', case = False)].copy()
	df_non_water = df_beverages[~(df_beverages.categories_tags.str.contains('en:spring-waters', case = False))].copy()
	return df_water, df_non_water


def protein_to_zero(product):
	neg =  nutri_sc.computeNegativePoints(product)
	fruits = nutri_sc.computeFruitsScore(product)
	fibers = nutri_sc.computeFibersScore(product)
	if neg < 11 or fruits == 5 or product.categories_tags.str.contains('cheese', case=False)[0]:
		return False
	else:
		return True

def clean_protein_case(df_non_beverages):
	df_non_beverages_no_prot = df_non_beverages.copy()
	for index in range(len(df_non_beverages_no_prot)):
		if protein_to_zero(df_non_beverages_no_prot.iloc[[index]]):
			df_non_beverages_no_prot.iat[index, 11] = 0 #Protein = 0
	return df_non_beverages_no_prot

def clean_fruit_case(df_product):
	df_product_fruit_complete = df_product.copy()
	for index in range(len(df_product_fruit_complete)):
		df_product_fruit_complete.iat[index, 8] = nutri_sc.getFruits(df_product_fruit_complete.iloc[[index]]) #Real Fruits
	return df_product_fruit_complete

def normalize_df(df_product_sum):
	df_normalize = df_product_sum.copy()
	quantites_tot = df_normalize['quantites'][0]
	if quantites_tot > 0:
		columns_df = df_normalize.columns
		for column in range(2, len(columns_df)):
			df_normalize[columns_df[column]] = df_normalize[columns_df[column]][0] * 100/ quantites_tot
		return df_normalize
	else:
		return df_product_sum

def api_fill(df_product, Api_list):
	df_product_api = df_product.copy()
	for name, quantites in Api_list:
		product = fill_from_Api(name)
		product['quantites'] = quantites
		df_product_api = df_product_api.append(product)
		
	return df_product_api


def main_nutri(list_product, data_food, Api_list):
	'''Compute NutriScore and take usefull value'''

	# Create and fill with API
	df_product = create_dataframe(list_product, data_food)
	df_product = api_fill(df_product, Api_list)

	# Put the fruits content on the real fruits-vegetables-nuts column
	df_product = clean_fruit_case(df_product)

	# Multiply each column by the quantites of the product 
	df_product = multpliply_quantites(df_product)

	# For recomendation, compute usefull values
	df_product_sum = sum_dataframe(df_product)

	Fiber_quantites = df_product_sum['fiber_100g'][0]
	Sodium_quantites = df_product_sum['sodium_100g'][0]
	Protein_quantites = df_product_sum['proteins_100g'][0]
	Energy_quantites = df_product_sum['energy_100g'][0]
	Glucide_quantites = df_product_sum['sugars_100g'][0]
	Lipid_quantites = df_product_sum['fat_100g'][0]
	nonbeverages_quantites = df_product_sum['quantites'][0]
	if nonbeverages_quantites != 0:
		Vegies_quantites = df_product_sum['fruits-vegetables-nuts_100g'][0] * 100/ df_product_sum['quantites'][0]
	else:
		Vegies_quantites = 0

	# Separate beverages and non-beverages and also the water
	df_beverages, df_non_beverages = separate_dataframe(df_product)
	df_water, df_non_water = separate_water(df_beverages)

	# Put protein egal to 0 according to the exception of the official NutriScore algorithm
	df_non_beverages = clean_protein_case(df_non_beverages)

	# Sum beverages
	df_beverages_tot = sum_dataframe(df_beverages)
	df_non_water_tot = sum_dataframe(df_non_water)
	df_water_tot = sum_dataframe(df_water)

	# For recomendation
	beverages_quantites = df_beverages_tot['quantites'][0]

	if beverages_quantites != 0:
		Non_water_quantites = df_non_water_tot['quantites'][0] * 100 / beverages_quantites
	else:
		Non_water_quantites = 0

	# Sum non-beverages
	df_non_beverages_tot = sum_dataframe(df_non_beverages)

	# Put the dataframe in a range of 0-100 (as a normal product)
	df_beverages_tot_norm = normalize_df(df_beverages_tot)
	df_non_beverages_tot_norm = normalize_df(df_non_beverages_tot)

	# compute NutriScore
	if (df_beverages_tot_norm['categories_tags'][0] != 0) & (len(df_non_water) > 0):
		final_score_Beverages = nutri_sc.computeScoreBeverages(df_beverages_tot_norm)
		NutriScore_Beverages = nutri_sc.getNutriScoreBeverages(final_score_Beverages, df_beverages_tot_norm)
	elif (len(df_non_water) == 0) & (len(df_water) > 0):
		final_score_Beverages, NutriScore_Beverages = '-', 'a'
	else:
		final_score_Beverages, NutriScore_Beverages = None, None

	if (df_non_beverages_tot_norm['categories_tags'][0] != 0) & (len(df_non_beverages) > 0):
		final_score_Non_Beverages = nutri_sc.computeScore(df_non_beverages_tot_norm)
		NutriScore_Non_Beverages = nutri_sc.getNutriScore(final_score_Non_Beverages)
	else:
		final_score_Non_Beverages, NutriScore_Non_Beverages = None, None

	Dict_ = {
	'Score_Beverages' : final_score_Beverages,
	'NutriScore_Beverages' : NutriScore_Beverages,
	'Score_Non_Beverages' : final_score_Non_Beverages,
	'NutriScore_Non_Beverages' : NutriScore_Non_Beverages,
	'Beverages_quantites' : beverages_quantites,
	'Soda_ratio' : Non_water_quantites,
	'Fruits' : Vegies_quantites,
	'Fiber' : Fiber_quantites,
	'Sodium' : Sodium_quantites,
	'Protein' : Protein_quantites,
	'Energy' : Energy_quantites,
	'Sugar' : Glucide_quantites,
	'Fat' : Lipid_quantites
	}

	#return df_water, df_product, df_beverages_tot, df_non_beverages_tot, Dict_
	return Dict_
