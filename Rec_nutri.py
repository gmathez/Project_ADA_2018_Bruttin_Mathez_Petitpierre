from df_nutri_create import sum_dataframe

# Compute recomendation for each categories
def Energy_rec(Male, Exercice, Age):
	if (Age >= 1) & (Age < 4):
		if Exercice == 1.4:
			if Male:
				return 1200

			else:
				return 1100


		elif Exercice == 1.6:
			if Male:
				return 1300

			else:
				return 1200

		else:
			return -1


	elif (Age >= 4) & (Age < 7):
		if Exercice == 1.4:
			if Male:
				return 1400

			else:
				return 1300

		elif Exercice == 1.6:
			if Male:
				return 1600

			else:
				return 1500

		elif Exercice == 1.8:
			if Male:
				return 1800

			else:
				return 1700
			
		else:
			return -1


	elif (Age >= 7) & (Age < 10):
		if Exercice == 1.4:
			if Male:
				return 1700

			else:
				return 1500

		elif Exercice == 1.6:
			if Male:
				return 1900

			else:
				return 1800

		elif Exercice == 1.8:
			if Male:
				return 2100

			else:
				return 2000
			
		else:
			return -1


	elif (Age >= 10) & (Age < 13):
		if Exercice == 1.4:
			if Male:
				return 1900

			else:
				return 1700

		elif Exercice == 1.6:
			if Male:
				return 2200

			else:
				return 2000

		elif Exercice == 1.8:
			if Male:
				return 2400

			else:
				return 2200
			
		else:
			return -1 


	elif (Age >= 13) & (Age < 15):
		if Exercice == 1.4:
			if Male:
				return 2300

			else:
				return 1900

		elif Exercice == 1.6:
			if Male:
				return 2600

			else:
				return 2200

		elif Exercice == 1.8:
			if Male:
				return 2900

			else:
				return 2500
			
		else:
			return -1


	elif (Age >= 15) & (Age < 19):
		if Exercice == 1.4:
			if Male:
				return 2600

			else:
				return 2000

		elif Exercice == 1.6:
			if Male:
				return 3000

			else:
				return 2300

		elif Exercice == 1.8:
			if Male:
				return 3400

			else:
				return 2600
			
		else:
			return -1


	elif (Age >= 19) & (Age < 25):
		if Exercice == 1.4:
			if Male:
				return 2400

			else:
				return 1900

		elif Exercice == 1.6:
			if Male:
				return 2800

			else:
				return 2200

		elif Exercice == 1.8:
			if Male:
				return 3100

			else:
				return 2500
			
		else:
			return -1


	elif (Age >= 25) & (Age < 51):
		if Exercice == 1.4:
			if Male:
				return 2300

			else:
				return 1800

		elif Exercice == 1.6:
			if Male:
				return 2700

			else:
				return 2100

		elif Exercice == 1.8:
			if Male:
				return 3000

			else:
				return 2400
			
		else:
			return -1


	elif (Age >= 51) & (Age < 65):
		if Exercice == 1.4:
			if Male:
				return 2200

			else:
				return 1700

		elif Exercice == 1.6:
			if Male:
				return 2500

			else:
				return 2000

		elif Exercice == 1.8:
			if Male:
				return 2800

			else:
				return 2200
			
		else:
			return -1


	elif (Age >= 65) & (Age < 120):
		if Exercice == 1.4:
			if Male:
				return 2100

			else:
				return 1700

		elif Exercice == 1.6:
			if Male:
				return 2500

			else:
				return 1900

		elif Exercice == 1.8:
			if Male:
				return 2800

			else:
				return 2100
			
		else:
			return -1


	else:
		return -1

def Lipid_rec(Age):
	if (Age >= 1) & (Age < 4):
		return (30, 40)
	elif (Age >= 4) & (Age < 15):
		return (30, 35)
	elif (Age >= 15) & (Age < 120):
		return(30, 31)
	else:
		return (-1, -1)

def Protein_rec(Male, Age):
	if (Age >= 1) & (Age > 4):
		return 1.0
	elif (Age >= 4) & (Age < 15):
		return 0.9
	elif (Age >= 15) & (Age < 19):
		if Male:
			return 0.9
		else:
			return 0.8
	elif (Age >= 19) & (Age < 65):
		return 0.8
	elif (Age >= 65) & (Age < 120):
		return 1.0
	else:
		return -1

def Water_rec(Age):
	if (Age >= 1) & (Age < 4):
		return 820
	elif (Age >= 4) & (Age < 7):
		return 940
	elif (Age >= 7) & (Age < 10):
		return 970
	elif (Age >= 10) & (Age < 13):
		return 1170
	elif (Age >= 13) & (Age < 15):
		return 1330
	elif (Age >= 15) & (Age < 19):
		return 1530
	elif (Age >= 19) & (Age < 25):
		return 1470
	elif (Age >= 25) & (Age < 51):
		return 1410
	elif (Age >= 51) & (Age < 65):
		return 1230
	elif (Age >= 65) & (Age < 120):
		return 1310
	else:
		return -1

def Fiber_rec(Fiber_quantites):
	return (Fiber_quantites, 30)

def Sugar_rec():
	return (45, 55)

def Sodium_rec(Age):
	if (Age >= 1) & (Age < 4):
		return 400 * 0.001
	elif (Age >= 4) & (Age < 7):
		return 500 * 0.001
	elif (Age >= 7) & (Age < 10):
		return 750 * 0.001
	elif (Age >= 10) & (Age < 13):
		return 1100 * 0.001
	elif (Age >= 13) & (Age < 15):
		return 1400 * 0.001
	elif (Age >= 15) & (Age < 120):
		return 1500 * 0.001
	else:
		return -1

# Compute text according to the recomendation for each categories
def Energy_text(Male, Exercice, Age, Energy_quantites, Days):
	rec = Energy_rec(Male, Exercice, Age)
	if rec != -1:
		rec = rec * 4.1868 # kcal to kJ
		if Energy_quantites > (rec * 1.1 * Days):
			return 'With an energy intake of {:.1f} kJ in {} days ({:.1f}kJ daily), you are above the daily recommendation ({:.1f} kJ per days). You should eat less or differently.'\
			.format(Energy_quantites, Days, Energy_quantites/Days, rec)
		elif Energy_quantites < (rec * 0.9 * Days):
			return 'With an energy intake of {:.1f} kJ in {} days ({:.1f}kJ daily), you are below the daily recommendation ({:.1f} kJ per days). You should eat more.'\
			.format(Energy_quantites, Days, Energy_quantites/Days, rec)
		else:
			return 'With an energy intake of {:.1f} kJ in {} days ({:.1f}kJ daily), you perfectly comply with the daily recommendation ({:.1f} kJ per days). Keep it up !'\
			.format(Energy_quantites, Days, Energy_quantites/Days, rec)
	else:
		return 'The recommendation for energy has not been computed. Have you filled in all the information to get the recommendation ?'

def Lipid_text(Age, Lipid_quantites, Energy_quantites):
	if Energy_quantites > 0:
		ratio = (Lipid_quantites * 37/ Energy_quantites) * 100
		max_, min_ = Lipid_rec(Age)
		if (max_ != -1) or (min_ != -1):
			if (ratio <= max_) & (ratio >= min_):
				return 'Your fat intake is fine ! Fats correspond to  {:.1f} % of your energy intake (for a recommended ratio of {} % to {} %. Keep it up !'\
				.format(ratio, min_, max_)
			elif ratio < min_:
				return 'Your fat intake ({:.1f} %) is low compared to the recommended ratio. It should be between {} % and {} %.'\
				.format(ratio, min_, max_)
			else:
				return 'Your fat intake ({:.1f} %) is high compared to the recommended ratio. It should be between {} % and {} %.'\
				.format(ratio, min_, max_)
		else:
			return 'The recommendation for fats has not been computed. Have you filled in all the information to get the recommendation ?'
	else:
		return 'Whoopsies, your energy intake is 0 kJ. You\'d better eat something !'

def Prot_text(Male, Age, Protein_quantites, Weight, Days):
	if Weight > 0:
		ratio = Protein_quantites / (Weight * Days)
		rec = Protein_rec(Male, Age)
		if rec != -1:
			if ratio > (rec * 1.1):
				return 'Your protein intake is too high. You eat {:.3f} g/kg for a daily recommendation of {:.1f} g/kg.'\
				.format(ratio, rec)
			elif ratio < (rec * 0.9):
				return 'Your protein intake is too low. You eat {:.3f} g/kg for a daily recommendation of {:.1f} g/kg.'\
				.format(ratio, rec)
			else:
				return 'Your protein intake is perfect. You eat {:.3f} g/kg for a daily recommendation of {:.1f} g/kg.'\
				.format(ratio, rec)

	else:
		return 'Whoopsies, your weight is zero. Are you a human or a one-dimensional point ?'

def Water_text(beverages_quantites, soda_ratio, Days, Age):
	rec = Water_rec(Age)
	if rec != -1:
		if beverages_quantites > (rec * 1.1 * Days):
			return ''''You may be drinking too much ! You drink {:.1f} ml in {} days ({:.1f}ml daily), while the daily recommendation is {:.1f} ml.
			Your cosumption of drinks other than water (eg. sodas) is {:.1f} % of your total amount of beverages.'''.format(beverages_quantites, Days, beverages_quantites/Days, rec, soda_ratio)
		elif beverages_quantites < (rec * 0.9 * Days):
			return '''You may not drink enough ! You drink {:.1f} ml in {} days ({:.1f}ml daily), while the daily recommendation is {:.1f} ml.
			Your cosumption of drinks other than water (eg. sodas) is {:.1f} % of your total amount of beverages.'''.format(beverages_quantites, Days, beverages_quantites/Days, rec, soda_ratio)
		else:
			return '''You drink properly ! You drink {:.1f} ml in {} days ({:.1f}ml daily), for a daily recommendation of {:.1f} ml.
			Your consumption of drinks other than water (eg. sodas) is {:.1f} % of your total amount of beverages.'''.format(beverages_quantites, Days, beverages_quantites/Days, rec, soda_ratio)
	else:
		return 'Whoopsies, our team of experts think you are either a fetus or a white walker. Not an exact science, though.'

def Fiber_text(Fiber_quantites, Days):
	rec = Fiber_rec(Fiber_quantites)
	if rec[0] > (rec[1] * 1.1 * Days):
		return 'You eat too much fibers. You should eat daily {:.1f} g but you eat {:.1f} g in {} days ({:.1f}g daily).'.format(rec[1], rec[0], Days, rec[0]/Days)
	elif rec[0] < (rec[1] * 0.9 * Days):
		return 'You do not eat enough fibers. You should eat daily {:.1f} g but you eat {:.1f} g in {} days ({:.1f}g daily).'.format(rec[1], rec[0], Days, rec[0]/Days)
	else:
		return 'You eat fibers to perfection. You should eat daily {:.1f} g and you eat {:.1f} g in {} days ({:.1f}g daily).'.format(rec[1], rec[0], Days, rec[0]/Days)

def Sugar_text(Sugar_quantites, Days):
	rec = Sugar_rec()
	if Sugar_quantites > (rec[1] * 1.1 * Days):
		return 'You eat too much sugar. You should eat less than {:.1f} g daily but you eat {:.1f} g in {} days ({:.1f}g daily).'.format(rec[1], Sugar_quantites, Days, Sugar_quantites/Days)
	elif Sugar_quantites < (rec[0] * 0.9 * Days):
		return 'You do not eat enough sugar. You should more eat than {:.1f} g daily but you eat {:.1f} g in {} days ({:.1f}g daily).'.format(rec[0], Sugar_quantites, Days, Sugar_quantites/Days)
	else:
		return 'You eat sugar at the perfection. You should eat between {:.1f} g daily and {:.1f} g. You eat {:.1f} g in {} days ({:.1f}g daily).'.format(rec[0], rec[1], Sugar_quantites, Days, Sugar_quantites/Days)

def Sodium_text(Age, Sodium_quantites, Days):
	rec = Sodium_rec(Age)
	if rec != -1:
		if Sodium_quantites > (rec * 1.1 * Days):
			return 'You eat too salty. You eat {:.1f} mg of sodium in {} days ({:.1f}mg daily) for a daily recommendation of {:.1f} mg.'\
			.format(Sodium_quantites * 1000, Days, Sodium_quantites * 1000/Days, rec * 1000)
		elif Sodium_quantites < (rec * 0.9 * Days):
			return 'You do not eat enough sodium. You eat {:.1f} mg of sodium {} days ({:.1f}mg daily) for a daily recommendation of {:.1f} mg.'\
			.format(Sodium_quantites * 1000, Days, Sodium_quantites * 1000/Days, rec * 1000)
		else:
			return 'Your sodium intake is perfect. You eat {:.1f} mg of sodium in {} days ({:.1f}mg daily) for a daily recommendation of {:.1f} mg.'\
			.format(Sodium_quantites * 1000, Days, Sodium_quantites * 1000/Days, rec * 1000)
	else:
		return 'The recommendation for the sodium was not computed. Did you put in all the information to have a recommendation ?'

def Fruits_text(Fruits_ratio):
	return 'Your menu is composed of {:.1f} % of fruits,vegetables and/or nuts.'.format(Fruits_ratio)

def Rec_text(Male, Age, Exercice, Days, Weight, Dict_):
	'''Main function to do the text for the recomendation'''
	Energy_quantites = Dict_['Energy']
	Lipid_quantites = Dict_['Fat']
	Protein_quantites = Dict_['Protein']
	Beverages_quantites = Dict_['Beverages_quantites']
	Fiber_quantites = Dict_['Fiber']
	Sugar_quantites = Dict_['Sugar']
	Sodium_quantites = Dict_['Sodium']
	Soda_ratio = Dict_['Soda_ratio']
	Fruits_ratio = Dict_['Fruits']

	Energy = Energy_text(Male, Exercice, Age, Energy_quantites, Days)
	Lipid = Lipid_text(Age, Lipid_quantites, Energy_quantites)
	Prot = Prot_text(Male, Age, Protein_quantites, Weight, Days)
	Water = Water_text(Beverages_quantites, Soda_ratio, Days, Age)
	Fiber = Fiber_text(Fiber_quantites, Days)
	Sugar = Sugar_text(Sugar_quantites, Days)
	Sodium = Sodium_text(Age, Sodium_quantites, Days)
	Fruits = Fruits_text(Fruits_ratio)


	text = '<h2 style="color:#3C627E"> Recommendation </h2>'
	text_energy = '<h3 style="color:#008080">Energy</h3>' + Energy
	text_lipid = '<h3 style="color:#008080">Lipid</h3>' + Lipid
	text_prot = '<h3 style="color:#008080">Protein</h3>' + Prot
	text_water = '<h3 style="color:#008080">Water</h3>' + Water
	text_fiber = '<h3 style="color:#008080">Fiber</h3>' + Fiber
	text_sugar = '<h3 style="color:#008080">Sugar</h3>' + Sugar
	text_sodium = '<h3 style="color:#008080">Sodium</h3>' + Sodium
	text_fruits = '<h3 style="color:#008080">Fruits - Vegetables - Nuts</h3>' + Fruits

	text_end = '''<h4 style="color:#3C627E">Information</h4><p>The recommendation was computed according to the
	<a href="http://www.sge-ssn.ch/fr/science-et-recherche/denrees-alimentaires-et-nutriments/recommandations-nutritionnelles/valeurs-de-reference-dach/" target="_blanck"
	>Société Suisse de Nutrition (SSN) reference values [in French/Deutch/Italian]</a>. We do not provide any additional information
	regarding vitamins or additives. For vitamins, you can check out the SSN website. Concerning the additives that may be found in your products,
	we suggest you to see <a href="https://pages.rts.ch/emissions/abe/1371092-liste-des-principaux-additifs-alimentaires.html" target="_blanck">
	A Bon Entendeur (RTS) [in French]</a>. Also, if you are pregnant or an athlete, other recommendations may apply.
	These recommendations are not for medical use and have been computed from <a href="https://world.openfoodfacts.org/" target="_blanck">
	Open Food Facts</a> database.</p>'''

	return text + text_energy + text_sugar + text_lipid + text_prot + text_fruits + text_fiber + text_sodium + text_water + text_end
	


