import pandas as pd
from collections import Counter

def relevant_tag(dic, tags, threshold = 5):
    """ Returns the least frequent tag from the list, who however has more than 'threshold' 
    correspondancies in the database """
    
    # Init
    dict_, sort = {}, []
    
    for tag in tags:
        dict_[tag] = dic[tag]
    
    # Keep only tag which have more occurencies than threshold
    dict_ = {k: v for k, v in dict_.items() if v >= threshold}
    if len(dict_) > 0:
        # Returns the most relevant tags
        sort = sorted(dict_, key = dict_.get, reverse=False)
        return sort
    else :
        return None

def list_df_tags(data_food):
    """ List of all the tags found in the dataset. Count the number of occurences and rank them
        according to this number. """
    
    # Split the tags found in the categories_tags columns
    all_tags = [tags.split(',') for tags in list(data_food[['categories_tags']].dropna().categories_tags)]
    
    # Init
    list_tags = []
    
    # List them
    for tags in all_tags:
        for tag in tags:
            list_tags.append(tag)
    
    # Return the list by number of occurences 
    return dict(Counter(list_tags).most_common())

def find_healthier_product(product_tuple, df, dic_tag):
    ''' Replace the product by a product of the same category that has a better Nutriscore '''
    
    # Initialize variables
    best_tag = ''
    best_sc, best_product, best_code = 0, {}, ''
    
    # A boolean to check if the product has been replaced
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
    
    # Catch the best tag of the product
    tags = product.categories_tags.split(',')
    best_tags = relevant_tag(dic_tag, tags, 10)
    if best_tags != None:
        best_tag = best_tags[0]
    else:
        return False, best_product, best_sc, best_code, old_sc, new_gr
    
    # Take the products which are of the same kind as the product we want to fill
    df_similar = df[df.categories_tags.str.contains(best_tag, case = False)]
    
    for ind, row in df_similar.iterrows():
        
        # Check if one of the similar product is actually better that our product
        score = df_similar.loc[ind]['Predicted_NutriScore_score']
        
        if score < best_sc:
            best_sc = score
            best_product = df_similar.loc[ind]
            best_code = ind 
            replaced = True
            new_gr = best_product['Predicted_NutriScore_grade'].upper()
       
    return replaced, best_product, best_sc, best_code, old_sc, old_gr, new_gr

def Better_product_rec(list_product, df):
    text = '<h2 style="color:#3C627E"> Healthier Product </h2>'
    dic_tag = list_df_tags(df)
    for product in list_product:
        replaced, ideal_product, ideal_nutriscore, ideal_code, old_score, old_gr, new_gr = find_healthier_product(product, df, dic_tag)
        if replaced:
            text = text + '''<p>We suggest to you to replace the product "{}" by this other product 
            <a href="https://world.openfoodfacts.org/product/{}" target="_blank">{}</a> that has a better Nutri-Score.
            Your product has a grade of {} and the one that we suggest to you has a grade of {}.</p>'''\
            .format(df.loc[product[0]][0], ideal_code, ideal_product[0] + ' (' + ideal_product[-1] + ')',\
            old_gr, new_gr)
        else:
            text = text + '''<p>Your product "{}" is the best in its category.</p>'''.format(df.loc[product[0]][0])

    return text

