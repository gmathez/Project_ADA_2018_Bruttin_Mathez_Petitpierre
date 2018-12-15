# Imports
import pandas as pd
import computeNutriScore as nutri_sc
from API_US_agri import fill_from_Api

def create_dataframe(list_product, data_food):
	''' Create a dataframe that contains all the product selected by the user '''
	'''
		Inputs:
		list_product(list(tuple[0](str))): Barcode of the product
		list_product(list(tuple[1](quantities))): Quantities of product ingested
		data_food(pandas dataframe): Dataframe containing all products

		Output:
		df_product(pandas dataframe): Dataframe containing all selected products
	'''

	# List of useful columns we want to keep
	column_for_data_food = ['product_name','categories_tags','energy_100g','fat_100g',
                        'saturated-fat_100g','sugars_100g','salt_100g','sodium_100g',
                        'fruits-vegetables-nuts_100g','fruits-vegetables-nuts-estimate_100g',
                        'fiber_100g','proteins_100g', 'quantites']

    # Create a pandas dataframe
	df_product = pd.DataFrame(columns = column_for_data_food)

	# Add each selected product to this new dataframe
	for barcode, quantites in list_product:
		df_product = df_product.append(data_food.loc[barcode])
		df_product.loc[barcode, 'quantites'] = quantites

	return df_product[column_for_data_food]


def multpliply_quantites(df_product):
	''' Multiply the nutrients quantities by the multiplication factor indicated by the user '''
	'''
		Input:
		df_product(pandas dataframe): Dataframe containing selected products

		Output:
		df_product(pandas dataframe): Dataframe containing selected products, with adjusted nutrients quantities
	'''

	# Iterate over all products
	for index in range(len(df_product)):
		quantites = df_product.iat[index, 12]

		# For each product, iterate over quantities
		for column in range(2, len(df_product.columns)):

			# Multiply the nutrients by the correct quantities
			if (df_product.columns[column] != 'quantites'):
				df_product.iat[index, column] = df_product.iat[index, column]  * quantites / 100

	return df_product


def sum_dataframe(df_product):
	''' Compute the total ingested quantity for each nutrient '''
	'''
		Input:
		df_product(pandas dataframe): Dataframe containing all selected products and their nutrients

		Output:
		(pandas dataframe): Dataframe containing the total ingested quantity for each nutrient
	'''

	# Copy dataframe
	df_product_copy = df_product.copy()

	# Column-wise sum of all products' nutrients
	sum_ = df_product_copy.sum()

	return pd.DataFrame(sum_.values, index = sum_.index).T


def separate_dataframe(df_product):
	''' Separate beverages and non-beverages product in two different dataframes '''
	'''
		Input:
		df_product(pandas dataframe): Dataframe containing all selected products

		Outputs:
		df_beverages(pandas dataframe): Dataframe containing all selected beverages products
		df_non_beverages(pandas dataframe): Dataframe containing all selected non-beverages products
	'''

	# Place all beverages products in one dataframe
	df_beverages = df_product[df_product.categories_tags.str.contains('beverages', case=False) &\
        ~df_product.categories_tags.str.contains('en:plant-based-foods,', case=False) &\
        (~ df_product.categories_tags.str.contains('milk', case=False))].copy()

    # Place all non-beverages products in one dataframe
	df_non_beverages = df_product[~(df_product.categories_tags.str.contains('beverages', case=False) &\
        ~df_product.categories_tags.str.contains('en:plant-based-foods,', case=False) &\
        (~ df_product.categories_tags.str.contains('milk', case=False)))].copy()

	return df_beverages, df_non_beverages


def separate_water(df_beverages):
	''' Separate water and non-water beverages in two different dataframes '''
	'''
		Input:
		df_beverages(pandas dataframe): Dataframe containing all selected beverages products

		Outputs:
		df_water(pandas dataframe): Dataframe containing all selected water beverages
		df_non_water(pandas dataframe): Dataframe containing all selected non-water beverages
	'''

	df_water = df_beverages[df_beverages.categories_tags.str.contains('en:spring-waters', case = False)].copy()
	df_non_water = df_beverages[~(df_beverages.categories_tags.str.contains('en:spring-waters', case = False))].copy()
	
	return df_water, df_non_water


def protein_to_zero(product):
	''' Check if the proteins should be taken into account or not '''
	'''
		Input:
		product(pandas dataframe row): Product raw from the dataframe (must be non-beverages)

		Output:
		(bool): Proteins should be set to zero (True/False)
	'''

	neg =  nutri_sc.computeNegativePoints(product)
	fruits = nutri_sc.computeFruitsScore(product)

	# If the total of negative points is >= 11, the proteins should not be taken into account
	# There are exceptions (e.g for cheese)
	if neg < 11 or fruits == 5 or product.categories_tags.str.contains('cheese', case=False)[0]:
		return False
	else:
		return True


def clean_protein_case(df_non_beverages):
	''' Check if the proteins should be set to zero or not '''
	'''
		Input:
		df_non_beverages(pandas dataframe): All selected non-beverages products

		Output:
		df_non_beverages_no_prot(pandas dataframe): Same dataframe with proteins removed when applicable
	'''

	# Copy dataframe
	df_non_beverages_no_prot = df_non_beverages.copy()

	# Iterate over the products and set proteins to zero when applicable
	# (i.e for all solid food that have >= 11 negative points except for some exceptions, as for example cheese)
	for index in range(len(df_non_beverages_no_prot)):
		if protein_to_zero(df_non_beverages_no_prot.iloc[[index]]):
			df_non_beverages_no_prot.iat[index, 11] = 0 # Protein = 0

	return df_non_beverages_no_prot


def clean_fruit_case(df_product):
	''' Check if the proteins should be set to zero or not '''
	'''
		Input:
		df_product(pandas dataframe): All selected products

		Output:
		df_product_fruit_complete(pandas dataframe): Same dataframe with fruits content completed
	'''

	# Copy dataframe
	df_product_fruit_complete = df_product.copy()

	# Iterate over all products and complete with real fruits/vegs/nuts or an estimate of it
	for index in range(len(df_product_fruit_complete)):
		df_product_fruit_complete.iat[index, 8] = nutri_sc.getFruits(df_product_fruit_complete.iloc[[index]])

	return df_product_fruit_complete


def normalize_df(df_product_sum):
	''' Check if the proteins should be set to zero or not '''
	'''
		Input:
		df_product_sum(pandas dataframe): Dataframe containing the summed-up nutrients columns

		Output:
		df_normalize(pandas dataframe): Same dataframe with normalized nutrients columns
	'''

	# Copy dataframe
	df_normalize = df_product_sum.copy()

	# Extract nutrients quantities from the dataframe
	quantites_tot = df_normalize['quantites'][0]

	# Check if the total nutrients quantities is not zero
	if quantites_tot > 0:

		# Iterate over columns
		columns_df = df_normalize.columns
		for column in range(2, len(columns_df)):

			# Normalize each nutrients columns by the total to obtain a percentage
			df_normalize[columns_df[column]] = df_normalize[columns_df[column]][0] * 100/ quantites_tot

		return df_normalize

	# Error handling: If the total of quantities is zero, we just return the input
	else:
		return df_product_sum


def api_fill(df_product, Api_list):
	''' Query the US Department of Agriculture API to fill the products '''
	'''
		Inputs:
		df_product(pandas dataframe): Dataframe containing all selected products
		Api_list(tuple[0](str)): Name of the products to fill from the API
		Api_list(tuple[1](int)): Quantities associated with those products

		Output:
		df_product_api(pandas dataframe): Products that have been queried by the API
	'''

	# Copy dataframe
	df_product_api = df_product.copy()

	# Iterate over all product and query the API in order query the products that have to be queried
	# (raw products)
	for name, quantites in Api_list:
		product = fill_from_Api(product_name = name)
		product['quantites'] = quantites
		df_product_api = df_product_api.append(product)
		
	return df_product_api


def main_nutri(list_product, data_food, Api_list):
	''' Take useful nutrients in the various products and compute the NutriScore '''
	'''
		Inputs:
		data_food(pandas dataframe): Dataframe containing all products
		list_product(list(tuple[0](str))): Barcode of the product
		list_product(list(tuple[1](quantities))): Quantities of product ingested
		Api_list(tuple[0](str)): Name of the products to fill from the API
		Api_list(tuple[1](int)): Quantities associated with those products
		
		Output:
		Dict_(dictionary): Returns the final scores of the products, as well as the quantities
			of nutrients ingested and all other useful information to deliver to the user
	'''

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
		Vegies_quantites = df_product_sum['fruits-vegetables-nuts_100g'][0] * 100 / df_product_sum['quantites'][0]
	else:
		Vegies_quantites = 0

	# Separate beverages and non-beverages and also the water in different dataframes
	df_beverages, df_non_beverages = separate_dataframe(df_product)
	df_water, df_non_water = separate_water(df_beverages)

	# Put protein to 0 when negative points are high,
	# except for the exceptions of the official NutriScore algorithm (e.g for cheese)
	df_non_beverages = clean_protein_case(df_non_beverages)

	# Sum beverages' nutrients
	df_beverages_tot = sum_dataframe(df_beverages)
	df_non_water_tot = sum_dataframe(df_non_water)
	df_water_tot = sum_dataframe(df_water)

	# Save the quantities of liquids that had been drunk
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

	# Compute NutriScore for beverages
	if (df_beverages_tot_norm['categories_tags'][0] != 0) & (len(df_non_water) > 0):
		final_score_Beverages = nutri_sc.computeScoreBeverages(df_beverages_tot_norm)
		NutriScore_Beverages = nutri_sc.getNutriScoreBeverages(final_score_Beverages, df_beverages_tot_norm)
	elif (len(df_non_water) == 0) & (len(df_water) > 0):
		final_score_Beverages, NutriScore_Beverages = '-', 'a'
	else:
		final_score_Beverages, NutriScore_Beverages = None, None

	# Compute NutriScore for non-beverages
	if (df_non_beverages_tot_norm['categories_tags'][0] != 0) & (len(df_non_beverages) > 0):
		final_score_Non_Beverages = nutri_sc.computeScore(df_non_beverages_tot_norm)
		NutriScore_Non_Beverages = nutri_sc.getNutriScore(final_score_Non_Beverages)
	else:
		final_score_Non_Beverages, NutriScore_Non_Beverages = None, None

	# Arrange all data to be returned in a nice dictionary
	dict_ = {
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

	return dict_
