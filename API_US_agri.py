# Imports
import pandas as pd
from urllib.request import urlopen
import urllib.request
import json
import re
import numpy as np

def catch_nutriment_value(nutri_dict, id_):
    ''' Catch the value of a nutriment defined by its id_ '''
    '''
        Input :
        nutri_dict(dictionary): contains all nutrients information of a product
        id_(int): contains the id of the nutrient in the database

        Output :
        value(float): value of the asked nutrient
    '''

    # Init
    value = 0

    # Iterate over the nutrients to match the id with the corresponding nutrient
    for i in range(len(nutri_dict)):
        if int(nutri_dict[i]['nutrient_id']) == id_:
            value = float(nutri_dict[i]['value'])
                        
    return value

def catch_fruit_or_veg(raw_aliment):
    ''' Return 1 if the element is a fruit or a vegetable '''
    '''
        Input :
        raw_aliment(dictionary): product from the database

        Output :
        fruit_or_veg(float): returns the fruits/vegs/nuts content
    '''
    
    # Init
    fruit_or_veg = 0.

    # If the group (i.e. type) of the product is fruits, vegetables or nuts, we put the corresponding
    # fruits/vegs/nuts content to 1
    group = raw_aliment['group']
    if group == 'Fruits and Fruit Juices': fruit_or_veg = 1.
    elif group == 'Vegetables and Vegetable Products' :  fruit_or_veg = 1.
    elif group == 'Legumes and Legume Products' : fruit_or_veg = 1.
    
    return fruit_or_veg

def find_raw_aliment(search_dict):
    ''' Sometimes, the raw aliment is not the first to appear in search result, this function is there 
        to ensure that the raw aliment is preferred. '''
    '''
        Input :
        search_dict(dictionary): product from the database

        Output :
        fruit_or_veg(float): returns the fruits/vegs/nuts content
    '''
    
    # Init
    score_list = []
    aliment_list = search_dict['list']['item']
    bonus_list = ['Fruits and Fruit Juices','Vegetables and Vegetable Products','Legumes and Legume Products']
    best_score = 0
    
    # Attribute a score to each aliment that is more susceptible to be a raw aliment
    for i in range(len(aliment_list)):
        score = 0

        # Use keywords 'raw' and 'unprepared' to detect raw aliments
        if ('raw' in aliment_list[i]['name']) or ('unprepared' in aliment_list[i]['name']): 
            score += 1

        # Use group (i.e category) to detect raw aliments
        if (aliment_list[i]['group'] in bonus_list) : score += 1

        # Store the score in a list
        score_list.append(score)
    
    # Return the aliment which has the highest score (there can be several) and is also the upper in the list
    for i in range(len(aliment_list)):

        # NB the entries are also classified by relevance in the database, so that the upper entries
        # are more likely to be relevant
        if score_list[i] == max(score_list) : return aliment_list[i]

def scrap(query_, ds_='Standard%20Reference', type_ = 'b'):
    ''' Scrap nutriment values from US Agriculture department database '''
    '''
        Input :
        query(str): name of the product we want to query with the API (e.g 'pear')
        ds_(str): Data source. Must be either 'Branded Food Products' or 'Standard Reference'
        type_(str): Report type. [b]asic or [f]ull or [s]tats

        Output :
        fruit_or_veg(float): returns the fruits/vegs/nuts content
    '''

    # Init constant
    kcal_to_kJ = 4.184
    
    # Allow to handle spaces in query without any problem to establish url
    error_ = { "errors": { "error": [{
                "status": 400,
                "parameter": "results",
                "message": "Your search resulted in zero results.Change your parameters and try again" }]}}

    query_ = query_.replace(' ', '%20')
    
    # Parameters
    api_key_ = 'HOEmuSjOUY4TSTXC4DM3I9CeOXOtypKAfpqi8Fuv' # Official API key for access to US gov database
    format1_ = 'json' # Output format
    sort_ = 'r' # Sort by relevance
    max_ = '20' # Number of search result(s)
    offset_ = '0' # Beginning row in the result
    
    # Query the API (will list all the possible results)
    url_search = 'https://api.nal.usda.gov/ndb/search/' + '?format=' + format1_ + '&q=' + query_ + \
                '&max=' + max_ + '&sort=' + sort_ + '&offset=' + offset_ + '&ds=' + ds_ + '&api_key=' + api_key_ 

    
    f_search = urlopen(url_search)
    assert f_search.code == 200
    search_dict = json.loads(f_search.read())
    
    # Error handling
    if search_dict == error_:
        ds2_='Branded%20Food%20Products'
        url_search = 'https://api.nal.usda.gov/ndb/search/' + '?format=' + format1_ + '&q=' + query_ + \
                '&max=' + max_ + '&sort=' + sort_ + '&offset=' + offset_ + '&ds=' + ds2_ + '&api_key=' + api_key_ 
        
        f_search = urlopen(url_search)
        assert f_search.code == 200
        search_dict = json.loads(f_search.read())
        
        if search_dict == error_:
            return {'Name' : np.nan,'kJ': np.nan,'Proteins' : np.nan,'Sugars' : np.nan,'Sat_fats' : np.nan,'Fibers' : np.nan,
                    'Sodium': np.nan,'Lipids' : np.nan,'Fruit_Veg_content' : np.nan}
    
    
    # From the possible results list, we now have to choose the best product
    # NB: this could be another product than the top product from the list
    # In our case, we would like the find the most 'raw' product
    f_search = urlopen(url_search)
    assert f_search.code == 200
    search_dict = json.loads(f_search.read())
        
    # Find the most 'raw' element
    raw_aliment = find_raw_aliment(search_dict)
    
    # Identification number in the database
    ndbno_ = raw_aliment['ndbno'] 
    
    # Get the proper report and open it
    url_food_report = 'https://api.nal.usda.gov/ndb/reports/' + '?ndbno=' + ndbno_ + '&type=' + type_ + \
                                                                '&format=' + format1_ + '&api_key=' + api_key_ 

    f_food_report = urlopen(url_food_report)
    assert f_food_report.code == 200
    
    # Load report
    food_report_dict = json.loads(f_food_report.read())
    
    nutri_dict = food_report_dict['report']['food']['nutrients']
    
    
    # Catch nutriments using ID from the US database
    nutri_values = {
        'Name' : raw_aliment['name'],
        'kJ': catch_nutriment_value(nutri_dict, 208) * kcal_to_kJ,
        'Proteins' : catch_nutriment_value(nutri_dict, 203),
        'Sugars' : catch_nutriment_value(nutri_dict, 269),
        'Sat_fats' : catch_nutriment_value(nutri_dict, 606),
        'Fibers' : catch_nutriment_value(nutri_dict, 291),
        'Sodium' : catch_nutriment_value(nutri_dict, 307),
        'Lipids' : catch_nutriment_value(nutri_dict, 204),
        'Fruit_Veg_content' : catch_fruit_or_veg(raw_aliment)
    }
    
    return nutri_values 

def fill_from_Api(product_name):
    ''' This function uses the API from US Agriculture department to scrap information about the product '''
    '''
        Input :
        product_name(str): name of the product we want to query with the API (e.g 'pear')

        Output :
        product_fill[column_for_product](pandas dataframe row): Row from the dataframe containing the product
            with all information necessary to be compatible with the rest of the programm
    '''

    # The US database is ASCII-encoded, while our should at least be latin-1
    # Therefore, we handle here the most frequent exceptions
    query = product_name
    query = re.sub('[éèêëÈÉÊË]', 'e', query)
    query = re.sub('[àáâãäåæÀÁÂÃÄÅÆ]', 'a', query)
    query = re.sub('[òóôõöøÒÓÔÕÖØ]', 'o', query)
    query = re.sub('[ùúûüÙÚÛÜ]', 'u', query)
    query = re.sub('[ìíîïÌÍÎÏ]', 'i', query)
    query = re.sub('[ýÿÝŸ]', 'y', query)
    query = re.sub('[ñÑ]', 'y', query)
    query = re.sub('[çÇ]', 'c', query)
    query = re.sub('[ß]', 'ss', query)
    query = re.sub('[$£ÞÐð]', '', query)
        
    # Scrap from the US database
    dic = scrap(query_ = query)
        
    # Format the result in the same system than openfoodfacts
    tags = ' '
    code = '000'
    columns = {
        'Name' : 'product_name',
        'kJ' : 'energy_100g',
        'Proteins': 'proteins_100g',
        'Sugars' : 'sugars_100g',
        'Sat_fats' : 'saturated-fat_100g',
        'Fibers': 'fiber_100g',
        'Sodium': 'sodium_100g',
        'Lipids' : 'fat_100g',
        'Fruit_Veg_content' : 'fruits-vegetables-nuts-estimate_100g'
    }

    # Only keep useful columns for the rest of the algorithm
    column_for_product = ['product_name','categories_tags','energy_100g',
                            'fat_100g','saturated-fat_100g','sugars_100g',
                            'salt_100g','sodium_100g','fruits-vegetables-nuts_100g',
                            'fruits-vegetables-nuts-estimate_100g','fiber_100g','proteins_100g']
    dic['code'] = code
    dic['categories_tags'] = tags
    dic['Sodium'] = dic['Sodium']*0.001 # mg => g
    dic['salt_100g'] = dic['Sodium']*2.5 # extrapolate salt from sodium
    if dic['Fruit_Veg_content'] == 1.:
        dic['Fruit_Veg_content'] = 100.0
    else:
        dic['Fruit_Veg_content'] = 0.0
    dic['fruits-vegetables-nuts_100g'] = np.nan
        
    # Fill the product with the new data
    product_fill = pd.DataFrame(data = dic, index = ['0']).set_index('code')
    product_fill.rename(columns=columns, inplace=True)
    
    return product_fill[column_for_product]

