#!/usr/bin/python

import pandas as pd
from tqdm import tqdm
from product_better import relevant_tag, list_df_tags
from computeNutriScore import computeNutriScore
import re
import numpy as np

def upload_df():
	url = 'https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv'
	return pd.read_csv(url, delimiter = '\t', low_memory = False)

def Compute_energy(fat, sugar, prot, fiber, margin):
    ''' Computes energy with a margin in kJ. source : https://en.wikipedia.org/wiki/Food_energy '''
    energy = (37 * fat + 17 * (sugar + prot) + 8 * fiber) - margin
    if energy < 0:
        return 0
    return energy

def set_coherent_values(df):
    """ Compute coherent value for food values. Set incoherent values to NaN or assign a valid value. """
    for i in tqdm(range(len(df)), ascii = True, desc = "coherent value"):
        
        # energy
        value = df.iat[i, 2]
        if  value < 0 or value > 4000:
            df.iat[i, 2] = np.nan
        
        # other columns
        for column in range(3, len(df.columns)):
            value = df.iat[i, column]
            if (value < 0) or (value > 100):
                df.iat[i, column] = np.nan
                
        # Salt / Sodium (should be perfectly correlated)        
        if np.isnan(df.iat[i, 6]):
            if ~np.isnan(df.iat[i, 7]):
                if ((df.iat[i, 7] * 2.5) <= 100):
                    df.iat[i, 6] = df.iat[i, 7] * 2.5 # Salt = Sodium * 2.5
                else:
                    df.iat[i, 7] = np.nan # Sodium must be a error value
        else:
            if np.isnan(df.iat[i, 7]):
                if ((df.iat[i, 6] / 2.5) <= 100):
                    df.iat[i, 7] = df.iat[i, 6] / 2.5 # Sodium = Salt / 2.5
                else:
                    df.iat[i, 6] = np.nan # Salt must be a error value
        
        # Saturated Fat / Fats                   
        if df.iat[i, 4] > df.iat[i, 3]: #saturated fat > fat
            df.iat[i, 3] = df.iat[i, 4]
        
        # Fruit-Vegetables-Nut Real / Estimate
        if ~np.isnan(df.iat[i, 8]) & np.isnan(df.iat[i, 9]):
            df.iat[i, 9] = df.iat[i, 8] # Estimate fruits-vegetables-nuts = Real
        if ~np.isnan(df.iat[i, 8]) & (df.iat[i, 9] > df.iat[i, 8]):
            df.iat[i, 9] = df.iat[i, 8]
        
        # Energy
        Fat, Sugar, Prot, Fiber = 0,0,0, 0
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



if __name__ == '__main__':

	restart = False

	for i in tqdm(range(1), ascii = True, desc="Download"):
		data_raw = upload_df()

	data_clean = data_raw.copy()

	data_clean.drop_duplicates(subset = 'code', keep = False, inplace = True)
	data_clean.set_index('code', inplace = True)

	data_clean = data_clean[~data_clean.product_name.isna() & ~data_clean.categories_tags.isna()]

	column_for_data_food = ['product_name','categories_tags','energy_100g','fat_100g',
                        'saturated-fat_100g','sugars_100g','salt_100g','sodium_100g',
                        'fruits-vegetables-nuts_100g','fruits-vegetables-nuts-estimate_100g',
                        'fiber_100g','proteins_100g']

	data_food = data_clean[column_for_data_food]

	data_clean.drop(column_for_data_food, axis = 1, inplace = True)

	data_food = set_coherent_values(data_food)

	data_food = data_food[~(data_food.isnull().sum(axis = 1) >= 9) | (data_food.categories_tags.str.contains('beverages', case = False))]
	
	dic_tag = list_df_tags(data_food)
	
	if restart:
		median_per_tag = []
		tags_index = []

		threshold = 3
		element =[(key,value) for key, value in dic_tag.items() if value >= threshold]

		for i in tqdm(range(len(element)), ascii =True, desc ="Median compute"):

			key, value = element[i]
			tags_index.append(key)
			data_ = data_food[data_food.categories_tags.str.contains(key, case = False)]
			value_food = list(data_.median().values)
			value_fruitsvegnut = np.median(np.concatenate((data_[['fruits-vegetables-nuts_100g']].dropna(axis = 0).values,\
				data_[['fruits-vegetables-nuts-estimate_100g']].dropna(axis = 0).values)))
			value_food.append(value_fruitsvegnut)
			median_per_tag.append(value_food)

		column_for_tab_for_filling = ['energy_100g','fat_100g','saturated-fat_100g',
		                                            'sugars_100g','salt_100g','sodium_100g','fruits-vegetables-nuts_100g',
		                                            'fruits-vegetables-nuts-estimate_100g','fiber_100g','proteins_100g', 'fruits-vegetables-nuts-filling-estimate']
		tab_for_filling = pd.DataFrame(data = median_per_tag, index = tags_index, columns = column_for_tab_for_filling)
		
		tab_for_filling.to_csv('./data/tab_for_filling.csv')
	else:
		tab_for_filling = pd.read_csv('./data/tab_for_filling.csv')

	data_food_final = data_food.copy()

	for i in tqdm(range(len(data_food_final)), ascii = True, desc = "Filling"):
	    
		if data_food_final.iloc[i].isnull().sum() > 0:
	            
			tags = data_food_final.iloc[i].categories_tags.split(',')
			tag_list = relevant_tag(dic_tag, tags, threshold)
	        
			if tag_list != None:
	            # iterate on each tag to complete
				for tag_i in range(len(tag_list)):
					tag = tag_list[tag_i]

	                # Take product on the same 'type' as the product we want to fill
					average_ = tab_for_filling.loc[tag]
					for j in range(2,len(data_food_final.columns)):
						if j != 8 : # Not complete real fruits/vegetables/nuts
	                	# the column need to be fill
							if str(data_food_final.iat[i, j]) == 'nan':
								if j != 9 :
									column_name = data_food_final.columns[j]
	                        		# the same products have values
									if ~np.isnan(average_[column_name]):
										data_food_final.iat[i, j] = average_[column_name]
								else: #estimate fruits-vegetables-nuts
									if ~np.isnan(average_['fruits-vegetables-nuts-filling-estimate']):
										data_food_final.iat[i, j] = average_['fruits-vegetables-nuts-filling-estimate']
						
						if data_food_final.iloc[i].isnull().sum() == 0:
							break

					if data_food_final.iloc[i].isnull().sum() == 0:
						break

	data_food_final = set_coherent_values(data_food_final)

	data_food_final['Predicted_NutriScore_grade'] = np.nan
	data_food_final['Predicted_NutriScore_score'] = np.nan
	data_food_final['Brands'] = ' '

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

	    # add brands                               
		Brands = data_clean.at[product.index[0], 'brands']
		if str(Brands) != 'nan':
			data_food_final.loc[product.index[0], 'Brands'] = Brands


	data_food_final.to_csv('./data/OpenFoodFacts_final.csv')
	data_food_final.to_csv('./data/OpenFoodFacts_final.csv.gz', compression='gzip')
            




