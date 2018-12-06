from numpy import isnan

def getFruits(product):
    if ~ isnan(product['fruits-vegetables-nuts_100g'])[0]:
        fruits_content = product['fruits-vegetables-nuts_100g'][0]
    elif ~ isnan(product['fruits-vegetables-nuts-estimate_100g'])[0]:
        fruits_content = product['fruits-vegetables-nuts-estimate_100g'][0]
    elif product.categories_tags.str.contains('juices-and-nectars', case=False)[0]:
        fruits_content = 100
    elif product.categories_tags.str.contains('compote', case=False)[0]:
        fruits_content = 90
    elif product.categories_tags.str.contains('en:vegetables-based-foods', case=False)[0]:
        fruits_content = 85
    elif product.categories_tags.str.contains('jams', case=False)[0]:
        fruits_content = 50
    else:
        fruits_content = 0
    
    return fruits_content

def computeFruitsScoreBeverages(product):
    fruits_content = getFruits(product)

    if fruits_content < 0:
        fruit_score = 999
    elif fruits_content <= 40:
        fruit_score = 0
    elif fruits_content <= 60:
        fruit_score = 2
    elif fruits_content <= 80:
        fruit_score = 4
    elif fruits_content <= 100:
        fruit_score =  10
    else:
        fruit_score = 999
    
    return fruit_score   


def computeFruitsScore(product):
    fruits_content = getFruits(product)

    if fruits_content < 0:
        fruit_score = 999
    elif fruits_content <= 40:
        fruit_score = 0
    elif fruits_content <= 60:
        fruit_score = 1
    elif fruits_content <= 80:
        fruit_score = 2
    elif fruits_content <= 100:
        fruit_score =  5
    else:
        fruit_score = 999
    
    return fruit_score 

def computeFibersScore(product):
    fibers_content = product.fiber_100g[0]
    if isnan(fibers_content):
        fibers_content = -999
    
    if fibers_content < 0:
        fibers_score = 999
    elif fibers_content <= 0.9:
        fibers_score = 0
    elif fibers_content <= 1.9:
        fibers_score = 1
    elif fibers_content <= 2.8:
        fibers_score = 2
    elif fibers_content <= 3.7:
        fibers_score = 3
    elif fibers_content <= 4.7:
        fibers_score = 4
    else: 
        fibers_score = 5
    return fibers_score

def computeProteinsScore(product):
    prot_content = product.proteins_100g[0]
    if isnan(prot_content):
        prot_content = -999
    
    if prot_content < 0:
        prot_score = 990
    elif prot_content <= 1.6:
        prot_score = 0
    elif prot_content <= 3.2:
        prot_score = 1
    elif prot_content <= 4.8:
        prot_score = 2
    elif prot_content <= 6.4:
        prot_score = 3
    elif prot_content <= 8.0:
        prot_score = 4
    else: 
        prot_score = 5
    
    return prot_score

def computeEnergyScoreBeverages(product):
    energy_content = product.energy_100g[0]
    if isnan(energy_content):
        energy_content = -999
    
    if energy_content < 0: 
        energy_score = 999
    elif energy_content == 0:
        energy_score = 0
    elif energy_content <= 30:
        energy_score = 1
    elif energy_content <= 60:
        energy_score = 2
    elif energy_content <= 90:
        energy_score = 3
    elif energy_content <= 120:
        energy_score = 4
    elif energy_content <= 150:
        energy_score = 5
    elif energy_content <= 180:
        energy_score = 6
    elif energy_content <= 210:
        energy_score = 7
    elif energy_content <= 240:
        energy_score = 8
    elif energy_content <= 270:
        energy_score = 9
    else:
        energy_score = 10

    return energy_score

def computeEnergyScore(product):
    energy_content = product.energy_100g[0]
    if isnan(energy_content):
        energy_content = -999
    
    if energy_content < 0:
        energy_score = -999
    elif energy_content <= 335:
        energy_score = 0
    elif energy_content <= 670:
        energy_score = 1
    elif energy_content <= 1005:
        energy_score = 2
    elif energy_content <= 1340:
        energy_score = 3
    elif energy_content <= 1675:
        energy_score = 4
    elif energy_content <= 2010:
        energy_score = 5
    elif energy_content <= 2345:
        energy_score = 6
    elif energy_content <= 2680:
        energy_score = 7
    elif energy_content <= 3015:
        energy_score = 8
    elif energy_content <= 3350:
        energy_score = 9
    else:
        energy_score = 10

    return energy_score

def computeFatScore(product):
    if product.categories_tags.str.contains('en:fats', case=False)[0]:
        ags = product['saturated-fat_100g'][0]
        fat_content = product.fat_100g[0]
        if isnan(ags) or isnan(fat_content):
            fat_score = -999
        elif fat_content == 0:
            fat_score = 0
        else:
            fat_ratio = ags / fat_content

            if fat_ratio < 10:
                fat_score = 0
            elif fat_ratio < 16:
                fat_score = 1
            elif fat_ratio < 22:
                fat_score = 2
            elif fat_ratio < 28:
                fat_score = 3
            elif fat_ratio < 34:
                fat_score = 4
            elif fat_ratio < 40:
                fat_score = 5
            elif fat_ratio < 46:
                fat_score = 6
            elif fat_ratio < 52:
                fat_score = 7
            elif fat_ratio < 58:
                fat_score = 8
            elif fat_ratio < 64:
                fat_score = 9
            else:
                fat_score = 10

    else:
        ags = product['saturated-fat_100g'][0]
        if isnan(ags):
            ags = -999

        if ags < 0:
            fat_score = -999
        elif ags <= 1:
            fat_score = 0
        elif ags <= 2:
            fat_score = 1
        elif ags <= 3:
            fat_score = 2
        elif ags <= 4:
            fat_score = 3
        elif ags <= 5:
            fat_score = 4
        elif ags <= 6:
            fat_score = 5
        elif ags <= 7:
            fat_score = 6
        elif ags <= 8:
            fat_score = 7
        elif ags <= 9:
            fat_score = 8
        elif ags <= 10:
            fat_score = 9
        else:
            fat_score = 10

    return fat_score      

def computeSugarScoreBeverages(product):
    sugar_content = product.sugars_100g[0]
    if isnan(sugar_content):
        sugar_content = -999
    
    if sugar_content < 0:
        sugar_score = 999
    elif sugar_content == 0:
        sugar_score = 0
    elif sugar_content <= 1.5:
        sugar_score = 1
    elif sugar_content <=  3:
        sugar_score = 2
    elif sugar_content <= 4.5:
        sugar_score = 3
    elif sugar_content <= 6:
        sugar_score = 4
    elif sugar_content <= 7.5:
        sugar_score = 5
    elif sugar_content <= 9:
        sugar_score = 6
    elif sugar_content <= 10.5:
        sugar_score = 7
    elif sugar_content <= 12:
        sugar_score = 8
    elif sugar_content <= 13.5:
        sugar_score = 9
    else:
        sugar_score = 10
    
    return sugar_score

def computeSugarScore(product):
    sugar_content = product.sugars_100g[0]
    if isnan(sugar_content):
        sugar_content = -999
    
    if sugar_content < 0:
        sugar_score = -999
    elif sugar_content <= 4.5:
        sugar_score = 0
    elif sugar_content <= 9:
        sugar_score = 1
    elif sugar_content <=  13.5:
        sugar_score = 2
    elif sugar_content <= 18:
        sugar_score = 3
    elif sugar_content <= 22.5:
        sugar_score = 4
    elif sugar_content <= 27:
        sugar_score = 5
    elif sugar_content <= 31:
        sugar_score = 6
    elif sugar_content <= 36:
        sugar_score = 7
    elif sugar_content <= 40:
        sugar_score = 8
    elif sugar_content <= 45:
        sugar_score = 9
    else:
        sugar_score = 10

    return sugar_score

def computeSodiumScore(product):
    sodium_content = product.salt_100g[0]
    if isnan(sodium_content):
        sodium_content = product.sodium_100g[0] 
        if isnan(sodium_content):
            sodium_content = -999
        else: 
            sodium_content = sodium_content * 1000
    else:
        sodium_content = product.salt_100g[0] * 1000 / 2.5

    if sodium_content < 0:
        sodium_score = -999
    elif sodium_content <= 90:
        sodium_score = 0
    elif sodium_content <= 180:
        sodium_score = 1
    elif sodium_content <= 270:
        sodium_score = 2
    elif sodium_content <= 360:
        sodium_score = 3
    elif sodium_content <= 450:
        sodium_score = 4
    elif sodium_content <= 540:
        sodium_score = 5
    elif sodium_content <= 630:
        sodium_score = 6
    elif sodium_content <= 720:
        sodium_score = 7
    elif sodium_content <= 810:
        sodium_score = 8
    elif sodium_content <= 900:
        sodium_score = 9
    else:
        sodium_score = 10

    return sodium_score

# Compute Positive Score for non beverages product
def computePositivePoints(product, neg):
    fruits = computeFruitsScore(product)
    fibers = computeFibersScore(product)
    if neg < 11 or fruits == 5 or product.categories_tags.str.contains('cheese', case=False)[0]:
        proteins = computeProteinsScore(product)
    else:
        proteins = 0

    return fruits + fibers + proteins

# Compute Negative Score for non beverages product
def computeNegativePoints(product):
    # Verif units !!!
    energy = computeEnergyScore(product) # kJ/100g
    fat = computeFatScore(product) # g/100g
    sugar = computeSugarScore(product) # g/100g
    sodium = computeSodiumScore(product) # mg/100g

    return energy + fat + sugar + sodium

# Compute score for beverages
def computeScoreBeverages(product):
    energy = computeEnergyScoreBeverages(product)
    sugar = computeSugarScoreBeverages(product)
    fruits = computeFruitsScoreBeverages(product)

    return energy + sugar - fruits

# Compute score for non beverages products
def computeScore(product):
    negative_points =  computeNegativePoints(product) 
    positive_points  = computePositivePoints(product, negative_points)
    
    return negative_points - positive_points 

# Compute NutriScore for Beverages
def getNutriScoreBeverages(score, product):
    if product.categories_tags.str.contains('en:spring-waters', case = False)[0]:
        NutriScore = 'a'
    elif score < -900:
        NutriScore = 'Error'
    elif score <= 1:
        NutriScore = 'b'
    elif score <= 5:
        NutriScore = 'c'
    elif score <= 9:
        NutriScore = 'd'
    elif score <= 20:
        NutriScore = 'e'
    else:
        NutriScore = 'Error'
    
    return NutriScore

# Compute Nutriscore for non Beverage products
def getNutriScore(score):
    if score < -900:
        NutriScore = 'Error'
    elif score < 0:
        NutriScore = 'a'
    elif score <= 2:
        NutriScore = 'b'
    elif score <= 10:
        NutriScore = 'c'
    elif score <= 18:
        NutriScore = 'd'
    elif score <= 40:
        NutriScore = 'e'
    else:
        NutriScore = 'Error'

    return NutriScore

# Top function    
def computeNutriScore(product):

    if product.categories_tags.str.contains('beverages', case=False)[0] & \
        ~product.categories_tags.str.contains('en:plant-based-foods,', case=False)[0] &\
        (~ product.categories_tags.str.contains('milk', case=False)[0]):
        final_score = computeScoreBeverages(product)
        NutriScore = getNutriScoreBeverages(final_score, product)
    else:
        final_score = computeScore(product)            
        NutriScore = getNutriScore(final_score)

    return (NutriScore, final_score)     