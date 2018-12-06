from df_nutri_create import sum_dataframe


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

def Water_rec(beverages_quantites):
	return (beverages_quantites, 1440)

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

def Energy_text(Male, Exercice, Age, Energy_quantites, Days):
	rec = Energy_rec(Male, Exercice, Age)
	if rec != -1:
		rec = rec * 4.1868
		if Energy_quantites > (rec * 1.1 * Days):
			return 'With your {:.1f} kJ of energy, you are above the recommendation ({:.1f} kJ per days). You should eat less or differently.'\
			.format(Energy_quantites, rec)
		elif Energy_quantites < (rec * 0.9 * Days):
			return 'With your {:.1f} kJ of energy, you are bellow the recommendation ({:.1f} kJ per days). You should eat more.'\
			.format(Energy_quantites, rec)
		else:
			return 'With your {:.1f} kJ of energy, you are perfect with the recommendation ({:.1f} kJ per days). Continue like this'\
			.format(Energy_quantites, rec)
	else:
		return 'The recommendation for the energy was not compute. Did you put all the information to have a recommendation ?'

def Lipid_text(Age, Lipid_quantites, Energy_quantites):
	if Energy_quantites > 0:
		ratio = (Lipid_quantites * 37/ Energy_quantites) * 100
		max_, min_ = Lipid_rec(Age)
		if (max_ != -1) or (min_ != -1):
			if (ratio <= max_) & (ratio >= min_):
				return 'Your fat cosumption is fine ! The fats correspond to the {:.1f} % of your energy cosumption (for a recommendation from {} % to {} %. Continue like this'\
				.format(ratio, min_, max_)
			elif ratio < min_:
				return 'Your fat cosumption ({:.1f} %) is low compare with the recommendation. It should be between {} % and {} %.'\
				.format(ratio, min_, max_)
			else:
				return 'Your fat cosumption ({:.1f} %) is high compare with the recommendation. It should be between {} % and {} %.'\
				.format(ratio, min_, max_)
		else:
			return 'The recommendation for the fats was not compute. Did you put all the information to have a recommendation ?'
	else:
		return 'Oups your energy quantity is 0 kJ. Eat something !'

def Prot_text(Male, Age, Protein_quantites, Weight, Days):
	if Weight > 0:
		ratio = Protein_quantites/Weight
		rec = Protein_rec(Male, Age)
		if rec != -1:
			if ratio > (rec * 1.1 * Days):
				return 'Your proteins levels are too high. You eat {:.1f} g/kg for a recommendation of {:.1f} g/kg per days.'\
				.format(ratio, rec)
			elif ratio < (rec * 0.9 * Days):
				return 'Your proteins levels are too low. You eat {:.1f} g/kg for a recommendation of {:.1f} g/kg per days.'\
				.format(ratio, rec)
			else:
				return 'Your proteins levels are perfect. You eat {:.1f} g/kg for a recommendation of {:.1f} g/kg per days.'\
				.format(ratio, rec)

	else:
		return 'Oups your weight are 0. Are you a human ?'

def Water_text(beverages_quantites, Days):
	rec = Water_rec(beverages_quantites)
	if rec[0] > (rec[1] * 1.1 * Days):
		return 'You drink too much ! You drink {:.1f} ml but the recommendation is {:.1f} ml per days'.format(rec[0], rec[1])
	elif rec[0] < (rec[1] * 0.9 * Days):
		return 'You drink not enough ! You drink {:.1f} ml but the recommendation is {:.1f} ml per days'.format(rec[0], rec[1])
	else:
		return 'You drink in the right way ! You drink {:.1f} ml for a recommendation of {:.1f} ml per days'.format(rec[0], rec[1])

def Fiber_text(Fiber_quantites, Days):
	rec = Fiber_rec(Fiber_quantites)
	if rec[0] > (rec[1] * 1.1 * Days):
		return 'You eat too much fibers. You should eat {:.1f} g but you eat {:.1f} g.'.format(rec[1], rec[0])
	elif rec[0] < (rec[1] * 0.9 * Days):
		return 'You eat not enough fibers. You should eat {:.1f} g but you eat {:.1f} g.'.format(rec[1], rec[0])
	else:
		return 'You eat fibers at the perfection. You should eat {:.1f} g and you eat {:.1f} g.'.format(rec[1], rec[0])
def Sugar_text(Sugar_quantites, Days):
	rec = Sugar_rec()
	if rec[0] > (rec[1] * 1.1 * Days):
		return 'You eat too much sugars. You should eat {:.1f} g but you eat {:.1f} g.'.format(rec[1], rec[0])
	elif rec[0] < (rec[1] * 0.9 * Days):
		return 'You eat not enough sugars. You should eat {:.1f} g but you eat {:.1f} g.'.format(rec[1], rec[0])
	else:
		return 'You eat sugars at the perfection. You should eat {:.1f} g and you eat {:.1f} g.'.format(rec[1], rec[0])

def Sodium_text(Age, Sodium_quantites, Days):
	rec = Sodium_rec(Age)
	if rec != -1:
		if Sodium_quantites > (rec * 1.1 * Days):
			return 'You eat too salty. You eat {:.1f} mg for a recommendation of {:.1f} mg per days.'\
			.format(Sodium_quantites * 1000, rec * 1000)
		elif Sodium_quantites < (rec * 0.9 * Days):
			return 'You eat not enough salt. You eat {:.1f} mg for a recommendation of {:.1f} mg per days.'\
			.format(Sodium_quantites * 1000, rec * 1000)
		else:
			return 'Your salt amount is perfect. You eat {:.1f} mg for a recommendation of {:.1f} mg per days.'\
			.format(Sodium_quantites * 1000, rec * 1000)
	else:
		return 'The recommendation for the sodium was not compute. Did you put all the information to have a recommendation ?'

def Rec_text(Male, Age, Exercice, Days, Weight, Dict_):

	Energy_quantites = Dict_['Energy']
	Lipid_quantites = Dict_['Fat']
	Protein_quantites = Dict_['Protein']
	beverages_quantites = Dict_['Beverages_quantites']
	Fiber_quantites = Dict_['Fiber']
	Sugar_quantites = Dict_['Sugar']
	Sodium_quantites = Dict_['Sodium']

	Energy = Energy_text(Male, Exercice, Age, Energy_quantites, Days)
	Lipid = Lipid_text(Age, Lipid_quantites, Energy_quantites)
	Prot = Prot_text(Male, Age, Protein_quantites, Weight, Days)
	Water = Water_text(beverages_quantites, Days)
	Fiber = Fiber_text(Fiber_quantites, Days)
	Sugar = Sugar_text(Sugar_quantites, Days)
	Sodium = Sodium_text(Age, Sodium_quantites, Days)

	text = '<h2 style="color:#3C627E"> Recommendation </h2>'
	text_energy = '<h3 style="color:#008080">Energy</h3>' + Energy
	text_lipid = '<h3 style="color:#008080">Lipid</h3>' + Lipid
	text_prot = '<h3 style="color:#008080">Protein</h3>' + Prot
	text_water = '<h3 style="color:#008080">Water</h3>' + Water
	text_fiber = '<h3 style="color:#008080">Fiber</h3>' + Fiber
	text_sugar = '<h3 style="color:#008080">Sugar</h3>' + Sugar
	text_sodium = '<h3 style="color:#008080">Salt</h3>' + Sodium

	text_end = '''<h4 style="color:#3C627E">Information</h4><p>The recommendation was provided according to 
	<a href="http://www.sge-ssn.ch/fr/science-et-recherche/denrees-alimentaires-et-nutriments/recommandations-nutritionnelles/valeurs-de-reference-dach/" target="_blanck"
	>Société Suisse de Nutrition (SSN) [in French/Deutch/Italian]</a>. We do not provided to you supplementary information
	about vitamines or additiv. For the vitamins you can check on the SSN website. About the additiv that can appear into your products,
	we suggest to you to see <a href="https://pages.rts.ch/emissions/abe/1371092-liste-des-principaux-additifs-alimentaires.html" target="_blanck">
	A Bon Entendeur (RTS) [in French]</a>. Also if you are pregnant or athletic, some other recommendation can be applied.
	These recommendations are not for medical use and was compute from <a href="https://world.openfoodfacts.org/" target="_blanck">
	Open Food Facts</a> database.</p>'''

	return text + text_energy + text_sugar + text_lipid + text_prot + text_fiber + text_sodium + text_water + text_end
	


