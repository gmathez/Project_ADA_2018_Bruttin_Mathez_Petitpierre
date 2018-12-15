#!/usr/bin/python

# Imports
import pandas as pd
from tqdm import tqdm
from product_better import relevant_tag, list_df_tags
from computeNutriScore import computeNutriScore
import re
import numpy as np

def upload_df():
	''' Upload the dataset directly from the OpenFoodFacts url

		Output :
		(pandas dataframe): Full raw dataset from OpenFoodFacts
	'''
	url = 'https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv'
	return pd.read_csv(url, delimiter = '\t', low_memory = False)

def Compute_energy(fat, sugar, prot, fiber, margin = 150):
	''' Computes the minimal energy contained in a product (with a margin)
		on the base of the energetic nutrient contained in it
		source : https://en.wikipedia.org/wiki/Food_energy 

		Inputs:
		fat(float/int): Amount of fat contained in the product (in gr)
		sugar(float/int): Amount of sugar contained in the product (in gr)
		prot(float/int): Amount of proteins contained in the product (in gr)
		fiber(float/int): Amount of fibers contained in the product (in gr)
		margin(float/int): Margin of tolerance (default = 150)

		Output:
		energy(float)
	'''

    # Constants
    kJ_per_gr_fat = 37
    kJ_per_gr_sugar_or_prot = 17
    kJ_per_gr_fiber = 8

    # Minimal energy computation
    energy = (kJ_per_gr_fat * fat + kJ_per_gr_sugar_or_prot * (sugar + prot) + \
    	kJ_per_gr_fiber * fiber) - margin

    if energy < 0:
        return 0

    return energy

def set_coherent_values(df):
	''' Compute coherent value for food values. Set incoherent values to NaN or assign a valid value

		Input:
		df(pandas dataframe): OpenFoodFacts dataset to clean

		Output:
		df(pandas dataframe): cleaned dataset
	'''

    for i in tqdm(range(len(df)), ascii = True, desc = "coherent value"):
        
        # Energy value is considered outlying if it exceeds 4000 kJ
        value = df.iat[i, 2]
        if  value < 0 or value > 4000:
            df.iat[i, 2] = np.nan
        
        # Values per 100gr cannot be negative or exceeds 100gr
        for column in range(3, len(df.columns)):
            value = df.iat[i, column]
            if (value < 0) or (value > 100):
                df.iat[i, column] = np.nan

        # Constant
        salt_sodium_ratio = 2.5
                
        # Salt / Sodium ratio checking (should be perfectly correlated)        
        if np.isnan(df.iat[i, 6]):
            if ~np.isnan(df.iat[i, 7]):
                if ((df.iat[i, 7] * salt_sodium_ratio) <= 100):
                    df.iat[i, 6] = df.iat[i, 7] * salt_sodium_ratio

                # Error handling
                else:
                    df.iat[i, 7] = np.nan
        else:
            if np.isnan(df.iat[i, 7]):
                if ((df.iat[i, 6] / salt_sodium_ratio) <= 100):
                    df.iat[i, 7] = df.iat[i, 6] / salt_sodium_ratio

                # Error handling
                else:
                    df.iat[i, 6] = np.nan
        
        # Total saturated fats cannot exceed Total fats
        if df.iat[i, 4] > df.iat[i, 3]:
            df.iat[i, 3] = df.iat[i, 4]
        
        # Fruit-Vegetables-Nut Real / Estimate should be coherent
        if ~np.isnan(df.iat[i, 8]) & np.isnan(df.iat[i, 9]):
            df.iat[i, 9] = df.iat[i, 8]
        if ~np.isnan(df.iat[i, 8]) & (df.iat[i, 9] > df.iat[i, 8]):
            df.iat[i, 9] = df.iat[i, 8]
        
        # Energy is at minimum as big as the sum of the energy of the nutrients
        Fat, Sugar, Prot, Fiber = 0, 0, 0, 0
        if ~np.isnan(df.iat[i, 3]):
            Fat = df.iat[i, 3]
                
        if ~np.isnan(df.iat[i, 5]):
            Sugar = df.iat[i, 5]
                
        if ~np.isnan(df.iat[i, 11]):
            Prot = df.iat[i, 11]
            
        if ~np.isnan(df.iat[i, 10]):
            Fiber = df.iat[i, 10]
        
        energy_comput = Compute_energy(Fat, Sugar, Prot, Fiber, 150)
        
        if np.isnan(df.iat[i, 2]) | (df.iat[i, 2] < energy_comput):
            df.iat[i, 2] = energy_comput

    return df

'''
********************************************************************************************
******************************************* MAIN *******************************************
********************************************************************************************
'''

if __name__ == '__main__':

	# Init
	restart = False

	# Upload dataset from OpenFoodFacts
	for i in tqdm(range(1), ascii = True, desc="Download"):
		data_raw = upload_df()

	# Copy dataset
	data_clean = data_raw.copy()

	# Clean dataset
	data_clean.drop_duplicates(subset = 'code', keep = False, inplace = True)
	data_clean.set_index('code', inplace = True)

	# Drop columns where name or categories tags are missing
	data_clean = data_clean[~data_clean.product_name.isna() & ~data_clean.categories_tags.isna()]

	# Keep only useful columns
	column_for_data_food = ['product_name','categories_tags','energy_100g','fat_100g',
                        'saturated-fat_100g','sugars_100g','salt_100g','sodium_100g',
                        'fruits-vegetables-nuts_100g','fruits-vegetables-nuts-estimate_100g',
                        'fiber_100g','proteins_100g']

	data_food = data_clean[column_for_data_food]

	data_clean.drop(column_for_data_food, axis = 1, inplace = True)

	# Check incoherent values (e.g negative physical quantities, etc.)
	data_food = set_coherent_values(data_food)

	# Drop columns when the product has no correct values entered
	data_food = data_food[~(data_food.isnull().sum(axis = 1) >= 9) | (
		data_food.categories_tags.str.contains('beverages', case = False))]
	
	# List all existing tags and count the number of occurences of those tags
	dic_tag = list_df_tags(data_food)
	
	# New Computation of filling.csv (if restart is enabled)
	if restart:

		# Init
		median_per_tag = []
		tags_index = []
		threshold = 3
		element = [(key,value) for key, value in dic_tag.items() if value >= threshold]

		# Complete fruits-vegetables-nuts column
		for i in tqdm(range(len(element)), ascii =True, desc ="Median compute"):

			key, value = element[i]
			tags_index.append(key)
			data_ = data_food[data_food.categories_tags.str.contains(key, case = False)]
			value_food = list(data_.median().values)
			value_fruitsvegnut = np.median(np.concatenate((
				data_[['fruits-vegetables-nuts_100g']].dropna(axis = 0).values,\
				data_[['fruits-vegetables-nuts-estimate_100g']].dropna(axis = 0).values)))
			value_food.append(value_fruitsvegnut)
			median_per_tag.append(value_food)

		# Keep only columns that have to be filled
		column_for_tab_for_filling = ['energy_100g', 'fat_100g', 'saturated-fat_100g',
			'sugars_100g','salt_100g','sodium_100g','fruits-vegetables-nuts_100g',
			'fruits-vegetables-nuts-estimate_100g','fiber_100g','proteins_100g', 
			'fruits-vegetables-nuts-filling-estimate']

		tab_for_filling = pd.DataFrame(data = median_per_tag, index = tags_index, 
			columns = column_for_tab_for_filling)
		
		# Save tab to fill in csv format
		tab_for_filling.to_csv('./data/tab_for_filling.csv')

	# If we don't want to recompute filling.csv, just load the old one
	else:
		tab_for_filling = pd.read_csv('./data/tab_for_filling.csv')

	# Copy dataframe
	data_food_final = data_food.copy()

	# Filling algorithm – iterate over all products
	for i in tqdm(range(len(data_food_final)), ascii = True, desc = "Filling"):

		# Check if the dataset has to be completed
		if data_food_final.iloc[i].isnull().sum() > 0:
	        
	        # Compute a list of relevant tags in the product
			tags = data_food_final.iloc[i].categories_tags.split(',')
			tag_list = relevant_tag(dic_tag, tags, threshold)
	        
			if tag_list != None:

	            # Iterate on each tag to complete
				for tag_i in range(len(tag_list)):
					tag = tag_list[tag_i]

	                # Take products with the same tags as the product we want to fill
	                # And replace the value to be filled with the average
					average_ = tab_for_filling.loc[tag]

					# Replace the values in each column
					for j in range(2,len(data_food_final.columns)):

						# In that case, we don't complete real fruits/vegetables/nuts
						if j != 8 : 

	                	# The column need to be filled
							if str(data_food_final.iat[i, j]) == 'nan':
								if j != 9 :
									column_name = data_food_final.columns[j]

	                        		# The same products have values
									if ~np.isnan(average_[column_name]):
										data_food_final.iat[i, j] = average_[column_name]

								# Estimate fruits-vegetables-nuts
								else: 
									if ~np.isnan(average_[
										'fruits-vegetables-nuts-filling-estimate']):
										data_food_final.iat[i, j] = average_[
										'fruits-vegetables-nuts-filling-estimate']
						
						# Check if it is necessary to continue to iterate, else break
						if data_food_final.iloc[i].isnull().sum() == 0:
							break

					# Check if it is necessary to continue to iterate, else break
					if data_food_final.iloc[i].isnull().sum() == 0:
						break

	# Clean again the dataset from incoherent values
	data_food_final = set_coherent_values(data_food_final)

	# Init
	data_food_final['Predicted_NutriScore_grade'] = np.nan
	data_food_final['Predicted_NutriScore_score'] = np.nan
	data_food_final['Brands'] = ' '

	# Now, the dataset will be completed with NutriScore grade and score and brands name
	for i in tqdm(range(len(data_food_final)), ascii = True, desc = "NutriScore"):

		product = data_food_final.iloc[[i]]

	    # Compute NutriScore
		nutriscore, final_score = computeNutriScore(product)

	    # Complete the dataset with the computed values
		data_food_final.loc[product.index[0], 'Predicted_NutriScore_grade'] = nutriscore
		data_food_final.loc[product.index[0], 'Predicted_NutriScore_score'] = final_score

	    # Search for common feature for the product name with long name
		regex_group = re.search('(.*)(?=même code)', product.product_name[0])

		if regex_group != None:
			data_food_final.loc[product.index[0], 'product_name'] = regex_group.group(0)[:-1]

	    # Add brands                               
		Brands = data_clean.at[product.index[0], 'brands']
		if str(Brands) != 'nan':
			data_food_final.loc[product.index[0], 'Brands'] = Brands

	# Save dataset to csv format
	data_food_final.to_csv('./data/OpenFoodFacts_final.csv')
	data_food_final.to_csv('./data/OpenFoodFacts_final.csv.gz', compression='gzip')
            




