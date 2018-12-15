# Imports
import pandas as pd
from collections import Counter


def relevant_tag(dic, tags, threshold = 5):
    ''' Returns the least frequent tag from the list, who however has more than 'threshold' 
        correspondancies in the database

        Inputs:
        dic(dictionary): contains the list of tags and the number of products associated to it
        tags(list(string)): Contains all the tags of a product
        threshold: The minimal number of neighbor with the same tag in order to consider it relevant
            (default = 5)

        Output:
        sort(list): Sorted list of relevant tags (most relevant first)
    '''
    
    # Init
    dict_, sort = {}, []
    
    # Create a new dictionary dict_ which only contains the entries of dic
    # that correspond to the product's tags
    for tag in tags:
        if tag in dic:
            dict_[tag] = dic[tag]
    
    # Keep only tags which have more occurencies than the threshold
    dict_ = {k: v for k, v in dict_.items() if v >= threshold}

    if len(dict_) > 0:
        # Returns the most relevant tags
        sort = sorted(dict_, key = dict_.get, reverse=False)
        return sort

    else :
        return None


def list_df_tags(data_food):
    ''' List of all the tags found in the dataset. Count the number of occurences and rank them
        according to this number

        Input:
        data_food(pandas dataframe): Dataset containing all products

        Output:
        (dictionary): List of all tags counted by number of occurences
    '''
    
    # Split the tags found in the categories_tags columns
    all_tags = [tags.split(',') for tags in list(data_food[['categories_tags']].dropna().categories_tags)]
    
    # Init
    list_tags = []
    
    # List them
    for tags in all_tags:
        for tag in tags:
            if tag != '':
                list_tags.append(tag)
    
    # Return the list by number of occurences 
    return dict(Counter(list_tags).most_common())


def find_healthier_product(product_tuple, df, dic_tag):
    ''' Replace the product by a product of the same category that has a better Nutriscore

        Inputs:
        product_tuple(tuple[0](str)): Barcode of the product to be eventually replaced
        product_tuple(tuple[1](int)): Quantity of the product
        df(pandas dataframe): Dataset containing all products
        dic_tag(dictionary): List of all tags in the dataset counted by number of occurences

        Outputs:
        replaced(bool): The product was replaced by a healthier one (True/False)
        best_product(pandas dataframe row):  Product to eventually replace the input product
        best_sc(int): NutriScore of the best product
        best_code(str): Barcode of the best product
        old_sc(int): NutriScore of the input product
        old_gr(str): From 'a' to 'e', NutriScore of the input product
        new_gr(str): From 'a' to 'e', NutriScore of the best product
    '''
    
    # Initialize variable
    best_tag = ''
    replaced = False
    
    # Find the product in the dataset
    product = df.loc[product_tuple[0]]
    
    # Check the score & initialize params
    best_code = product_tuple[0]
    best_product = product
    best_sc = product['Predicted_NutriScore_score']
    old_sc = best_sc
    old_gr = product['Predicted_NutriScore_grade'].upper()
    new_gr = product['Predicted_NutriScore_grade'].upper()
    
    # Catch the input product's most relevant tag
    tags = product.categories_tags.split(',')
    best_tags = relevant_tag(dic_tag, tags, 10)
    if best_tags != None:
        best_tag = best_tags[0]

    # Error handling : the product to replace has no reliable tag
    else:
        return False, best_product, best_sc, best_code, old_sc, old_gr, new_gr
    
    # Take the products which are of the same kind as the product we want to fill
    df_similar = df[df.categories_tags.str.contains(best_tag, case = False)]
    
    for ind, row in df_similar.iterrows():
        
        # Check if one of the similar product is actually better that our product
        score = df_similar.loc[ind]['Predicted_NutriScore_score']
        grade = df_similar.loc[ind]['Predicted_NutriScore_grade']
        
        if (score < best_sc) & (grade != 'Error'):
            best_sc = score
            best_product = df_similar.loc[ind]
            best_code = ind 
            replaced = True
            new_gr = best_product['Predicted_NutriScore_grade'].upper()
       
    return replaced, best_product, best_sc, best_code, old_sc, old_gr, new_gr


def Better_product_rec(list_product, df):
    ''' Replace the product by a product of the same category that has a better Nutriscore

        Inputs:
        list_product(dictionary): List of the products entered by to user, to replace by healthier ones
        df(pandas dataframe): Dataset containing all products

        Output:
        text(str): Text of the replacement suggestion
    '''

    text = '<h2 style="color:#3C627E"> Healthier Product </h2>'
    dic_tag = list_df_tags(df)

    # Check for each product healthier product and compute the text for the recomendation
    for product in list_product:
        replaced, ideal_product, ideal_nutriscore, ideal_code, old_score, old_gr, new_gr = find_healthier_product(product, df, dic_tag)
        if replaced & (type(ideal_product[-1]) == 'str') & (type(ideal_product[0]) == 'str') :
            text = text + '''<p>We suggest that you replace the product "{}" with this other product 
            <a href="https://world.openfoodfacts.org/product/{}" target="_blank">{}</a> that has a better Nutri-Score.
            Your product has a grade of {} and the one  we suggest to you has a grade of {}.</p>'''\
            .format(str(df.loc[product[0]][0]), str(ideal_code), str(ideal_product[0]) + ' (' + str(ideal_product[-1]) + ')',\
            str(old_gr), str(new_gr))
        else:
            text = text + '''<p>Your product "{}" is the best in its category.</p>'''.format(df.loc[product[0]][0])

    return text


