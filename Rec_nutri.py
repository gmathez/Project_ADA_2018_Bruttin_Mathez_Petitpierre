# Import
from df_nutri_create import sum_dataframe


def Energy_rec(Male, Exercice, Age):
	''' Compute energy intake recommendation for each different user profile

	Inputs:
	Male(bool): True if the user is male, false if the user is female
	Exercice(float): Level of activity of the user
		(1.4 = static, 1.6 = average, 1.8 = active)
	Age(int): Age of the user

	Output:
	(int): Energy intake recommendation (in kcal)
	'''

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
	''' Compute Lipid intake recommendation for each different user profile

	Input:
	Age(int): Age of the user

	Output:
	(int, int): (min, max) Lipid intake recommendation (in gr)
	'''
	if (Age >= 1) & (Age < 4):
		return (30, 40)

	elif (Age >= 4) & (Age < 15):
		return (30, 35)

	elif (Age >= 15) & (Age < 120):
		return(30, 31)

	else:
		return (-1, -1)


def Protein_rec(Male, Age):
	''' Compute protein intake recommendation for each different user profile

	Inputs:
	Male(bool): True if the user is male, false if the user is female
	Age(int): Age of the user

	Output:
	(float): Protein intake recommendation (in gr per kg (weight of the user))
	'''

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
	''' Compute water intake recommendation for each different user profile

	Input:
	Age(int): Age of the user

	Output:
	(int): Water intake recommendation (in ml)
	'''

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


def Fiber_rec():
	''' Returns fiber intake recommendation

	Output:
	int: Fiber intake recommendation (in gr)
	'''
	return 30


def Sugar_rec():
	''' Returns sugar intake recommendation

	Output:
	(int, int): Sugar intake recommendation (in gr)
	'''
	return (45, 55)


def Sodium_rec(Age):
	''' Compute sodium intake recommendation for each different user profile

	Input:
	Age(int): Age of the user

	Output:
	(float): Sodium intake recommendation (in gr)
	'''

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
	''' Return text of the feedback for energy intake

	Inputs:
	Male(bool): True if the user is male, false if the user is female
	Exercice(float): Level of activity of the user
		(1.4 = static, 1.6 = average, 1.8 = active)
	Age(int): Age of the user
	Energy_quantities(int/float): Quantity of energy consumed (in kJ)
	Days(int): Number of days in which this energy was consumed

	Output:
	(str): Feedback on energy intake
	'''

	# Get energy intake recommendation
	rec = Energy_rec(Male, Exercice, Age)

	if rec != -1:

		# Conversion to kcal to facilitate the comparison with the reference values of the SSN
		kJ_to_kcal = 0.2388
		Energy_quantites = Energy_quantites * kJ_to_kcal

		# Return the appropriate feedback text
		if (Energy_quantites > (rec * 1.1 * Days)) & (Energy_quantites <= (rec * 1.3 * Days)):
			return '''With an energy intake of {:.1f} kcal in {} days ({:.1f} kcal daily), you are slightly above the 
			daily recommendation ({:.1f} kcal per days). 
			You should probably consider to eat less caloric food.'''\
			.format(Energy_quantites, Days, Energy_quantites/Days, rec)

		elif (Energy_quantites > (rec * 1.3 * Days)):
			return '''With an energy intake of {:.1f} kcal in {} days ({:.1f} kcal daily), you are largely above the 
			daily recommendation ({:.1f} kcal per days). 
			You should consider to eat less caloric food and reduce the amount of food ingested.'''\
			.format(Energy_quantites, Days, Energy_quantites/Days, rec)

		elif (Energy_quantites < (rec * 0.9 * Days)) & (Energy_quantites >= (rec * 0.7 * Days)):
			return '''With an energy intake of {:.1f} kcal in {} days ({:.1f} kcal daily), you are slightly below the 
			daily recommendation ({:.1f} kcal per days). 
			You should consider to eat more.'''\
			.format(Energy_quantites, Days, Energy_quantites/Days, rec)

		elif (Energy_quantites < (rec * 0.7 * Days)):
			return '''With an energy intake of {:.1f} kcal in {} days ({:.1f} kcal daily), you are largely below the 
			daily recommendation ({:.1f} kcal per days). 
			You should consider to eat more and to ingest more caloric food.'''\
			.format(Energy_quantites, Days, Energy_quantites/Days, rec)

		else:
			return '''With an energy intake of {:.1f} kcal in {} days ({:.1f} kcal daily), you perfectly comply with 
			the daily recommendation ({:.1f} kcal per days). Keep it up !'''\
			.format(Energy_quantites, Days, Energy_quantites/Days, rec)

	# Error handling
	else:
		return '''The recommendation for energy has not been computed. Have you filled in all the information to get 
		the recommendation ?'''


def Lipid_text(Age, Lipid_quantites, Energy_quantites):
	''' Return text of the feedback for lipid intake

	Inputs:
	Age(int): Age of the user
	Energy_quantities(int/float): Quantity of energy consumed (in kJ)
	Lipid_quantites(int/float): Quantity of lipid consumed (in gr)

	Output:
	(str): Feedback on lipid intake
	'''

	if Energy_quantites > 0 :

		# Compute the proportion of lipid energy intake in the total energy intake
		kJ_per_gr_lipids = 37.
		ratio = (Lipid_quantites * kJ_per_gr_lipids / Energy_quantites) * 100.

		# Get the lipid recommended intake (range)
		max_, min_ = Lipid_rec(Age)

		# Return the appropriate feedback text
		if (max_ != -1) or (min_ != -1):
			if (ratio <= max_) & (ratio >= min_):
				return '''Your fat intake is fine ! Fats correspond to  {:.1f} % of your energy intake (for a 
				recommended ratio of {} % to {} %. Keep it up !'''\
				.format(ratio, min_, max_)

			elif ratio < min_:
				return '''Your fat intake ({:.1f} %) is low compared to the recommended ratio.
				 It should be between {} % and {} %.'''\
				.format(ratio, min_, max_)

			else:
				return '''Your fat intake ({:.1f} %) is high compared to the recommended ratio.
				 It should be between {} % and {} %.'''\
				.format(ratio, min_, max_)
		else:
			return '''The recommendation for fats has not been computed.
			 Have you filled in all the information to get the recommendation ?'''

	# Error handling
	else:
		return '''Whoopsies, your energy intake is 0 kJ. You'd better eat something !'''


def Prot_text(Male, Age, Protein_quantites, Weight, Days):
	''' Return text of the feedback for protein intake

	Inputs:
	Male(bool): True if the user is male, false if the user is female
	Age(int): Age of the user
	Protein_quantites(int/float): Quantity of lipid consumed (in gr)
	Weight(int/float): Weight of the user (in kg)
	Days(int): Number of days in which these proteins were consumed

	Output:
	(str): Feedback on protein intake
	'''

	if Weight > 0:

		# Compute protein intake per kg per day
		ratio = Protein_quantites / (Weight * Days)

		# Get recommendation for daily protein intake
		rec = Protein_rec(Male, Age)

		# Return the appropriate feedback text
		if rec != -1:
			if (ratio > (rec * 1.1)) & (ratio <= (rec * 1.3)):
				return '''Your protein intake is slightly higher than the recommendation. You eat {:.3f} g/kg 
				for a daily recommendation of {:.1f} g/kg.'''\
				.format(ratio, rec)

			elif ratio > (rec * 1.3):
				return '''Your protein intake is clearly higher than the recommendation. You eat {:.3f} g/kg for 
				a daily recommendation of {:.1f} g/kg.'''\
				.format(ratio, rec)

			elif (ratio < (rec * 0.9)) & (ratio >= (rec * 0.7)):
				return '''Your protein intake is slightly too low. You eat {:.3f} g/kg for
				 a daily recommendation of {:.1f} g/kg.'''\
				.format(ratio, rec)

			elif (ratio < (rec * 0.7)):
				return '''Your protein intake is clearly too low. You eat {:.3f} g/kg for 
				a daily recommendation of {:.1f} g/kg.'''\
				.format(ratio, rec)

			else:
				return 'Your protein intake is perfect. You eat {:.3f} g/kg for a daily recommendation of {:.1f} g/kg.'\
				.format(ratio, rec)

	# Error handling
	else:
		return 'Whoopsies, your weight is zero. Are you a human or a one-dimensional point ?'


def Water_text(beverages_quantites, soda_ratio, Days, Age):
	''' Return text of the feedback for liquid intake

	Inputs:
	beverages_quantites(int/float): Quantity of liquid drunk (in ml)
	soda_ratio(float): Percentage of soda in the total liquid consumption
	Days(int): Number of days in which this liquid was consumed
	Age(int): Age of the user

	Output:
	(str): Feedback on liquid intake
	'''

	# Get recommendation for daily liquid intake
	rec = Water_rec(Age)

	# Return the appropriate feedback text
	if rec != -1:
		if beverages_quantites > (rec * 1.3 * Days):
			return '''You drink a little more than the actual recommendation. 
			You drink {:.1f} ml in {} days ({:.1f}ml daily), while the daily 
			recommendation is {:.1f} ml. Your consumption of drinks other than water (eg. sodas) is {:.1f} 
			% of your total amount of beverages.'''\
			.format(beverages_quantites, Days, beverages_quantites/Days, rec, soda_ratio)

		elif beverages_quantites < (rec * 0.7 * Days):
			return '''You drink a less than the actual recommendation. 
			You drink {:.1f} ml in {} days ({:.1f}ml daily), while the daily recommendation is {:.1f} ml.
			Your consumption of drinks other than water (eg. sodas) is {:.1f} % of your total amount of 
			beverages.'''\
			.format(beverages_quantites, Days, beverages_quantites/Days, rec, soda_ratio)

		else:
			return '''You drink properly ! You drink {:.1f} ml in {} days ({:.1f}ml daily), for a daily 
			recommendation of {:.1f} ml. Your consumption of drinks other than water (eg. sodas) is {:.1f} 
			% of your total amount of beverages.'''\
			.format(beverages_quantites, Days, beverages_quantites/Days, rec, soda_ratio)

	# Error handling
	else:
		return '''Whoopsies, our team of experts think you are either a fetus
		 or a white walker. Not an exact science, though.'''


def Fiber_text(Fiber_quantites, Days):
	''' Return text of the feedback for fibers intake

	Inputs:
	Fiber_quantites(float/int): Quantity of fibers consumed (in gr)
	Days(int): Number of days in which these fibers were consumed

	Output:
	(str): Feedback on fibers intake
	'''

	# Get fibers recommended intake
	rec = Fiber_rec()

	# Return the appropriate feedback text
	if (Fiber_quantites > (rec * 1.1 * Days)) & (Fiber_quantites <= (rec * 1.3 * Days)):
		return '''You eat slightly more fibers than the actual minimal recommendation. 
		Your daily consumption is {:.1f} g and the recommendation is {:.1f} g per day.'''\
		.format(Fiber_quantites/Days, rec)

	elif (Fiber_quantites > (rec * 1.3 * Days)):
		return '''You eat clearly more fibers than the actual minimal recommendation.  
		Your daily consumption is {:.1f} g and the recommendation is {:.1f} g per day.'''\
		.format(Fiber_quantites/Days, rec)

	elif Fiber_quantites < (rec * 0.9 * Days):
		return '''You do not eat enough fibers. Your 
		daily consumption shoud be {:.1f} g but you eat only {:.1f} g in {} days ({:.1f} g 
		daily).'''.format(rec, Fiber_quantites, Days, Fiber_quantites/Days)

	else:
		return '''You eat fibers to perfection. You should eat daily {:.1f} g and you eat {:.1f} g 
		in {} days ({:.1f} g daily).'''.format(rec, Fiber_quantites, Days, Fiber_quantites/Days)


def Sugar_text(Sugar_quantites, Days):
	''' Return text of the feedback for sugar intake

	Inputs:
	Sugar_quantites(float/int): Quantity of sugar consumed (in gr)
	Days(int): Number of days in which this sugar was consumed

	Output:
	(str): Feedback on sugars intake
	'''

	# Get sugar recommended intake
	rec = Sugar_rec()

	# Return the appropriate feedback text
	if Sugar_quantites > (rec[1] * 1.3 * Days):
		return '''You eat too much sugar. You should eat less than {:.1f} g daily but you eat actually {:.1f} 
		g in {} days ({:.1f} g daily).'''\
		.format(rec[1], Sugar_quantites, Days, Sugar_quantites/Days)

	elif (Sugar_quantites > (rec[1] * 1.1 * Days)) & (Sugar_quantites <= (rec[1] * 1.3 * Days)):
		return '''You eat slightly more sugar than the recommended limit. 
		You should eat less than {:.1f} g daily but you eat actually {:.1f} 
		g in {} days ({:.1f} g daily).'''\
		.format(rec[1], Sugar_quantites, Days, Sugar_quantites/Days)

	elif (Sugar_quantites < (rec[0] * 0.9 * Days)) & (Sugar_quantites >= (rec[0] * 0.7 * Days)):
		return '''You eat slightly less sugar than the recommended limit.  
		The consumption limit is {:.1f} g daily and you eat {:.1f} g in {} days ({:.1f} g daily).
		'''.format(rec[0], Sugar_quantites, Days, Sugar_quantites/Days)

	elif (Sugar_quantites < (rec[0] * 0.7 * Days)):
		return '''You eat clearly less sugar than the recommended limit. 
		The consumption limit is {:.1f} g daily and you eat {:.1f} g in {} days ({:.1f} g daily).
		'''.format(rec[0], Sugar_quantites, Days, Sugar_quantites/Days)

	# Error handling
	else:
		return '''You eat a normal amount of sugar. You should eat between {:.1f} g and {:.1f} g per day. 
		You eat {:.1f} g in {} days ({:.1f} g daily).'''\
		.format(rec[0], rec[1], Sugar_quantites, Days, Sugar_quantites/Days)


def Sodium_text(Age, Sodium_quantites, Days):
	''' Return text of the feedback for sodium intake

	Inputs:
	Age(int): Age of the user
	Sodium_quantites(float/int): Quantity of sodium consumed (in mg)
	Days(int): Number of days in which this sodium was consumed

	Output:
	(str): Feedback on sodium intake
	'''

	# Get sodium recommended intake
	rec = Sodium_rec(Age)

	# Return the appropriate feedback text
	if rec != -1:
		if Sodium_quantites > (rec * 1.3 * Days):
			return '''You eat too salty. You eat {:.1f} mg of sodium in {} days ({:.1f} mg daily) for 
			a daily recommendation of {:.1f} mg.'''\
			.format(Sodium_quantites * 1000, Days, Sodium_quantites * 1000/Days, rec * 1000)

		elif (Sodium_quantites > (rec * 1.1 * Days)) & (Sodium_quantites <= (rec * 1.3 * Days)):
			return '''You eat slightly more sodium than the recommendation.  
			You eat {:.1f} mg of sodium {} days ({:.1f} mg daily) for a daily recommendation of {:.1f} mg.'''\
			.format(Sodium_quantites * 1000, Days, Sodium_quantites * 1000/Days, rec * 1000)

		elif (Sodium_quantites < (rec * 0.9 * Days)) & (Sodium_quantites >= (rec * 0.7 * Days)):
			return '''You eat slightly less sodium than the recommendation.  
			You eat {:.1f} mg of sodium {} days ({:.1f} mg daily) for a daily recommendation of {:.1f} mg.'''\
			.format(Sodium_quantites * 1000, Days, Sodium_quantites * 1000/Days, rec * 1000)

		elif Sodium_quantites < (rec * 0.7 * Days):
			return '''You do not eat enough sodium. You eat {:.1f} mg of sodium {} days ({:.1f} mg daily) 
			for a daily recommendation of {:.1f} mg.'''\
			.format(Sodium_quantites * 1000, Days, Sodium_quantites * 1000/Days, rec * 1000)

		else:
			return '''Your sodium intake is perfect. You eat {:.1f} mg of sodium in {} days ({:.1f} mg daily) 
			for a daily recommendation of {:.1f} mg.'''\
			.format(Sodium_quantites * 1000, Days, Sodium_quantites * 1000/Days, rec * 1000)

	# Error handling
	else:
		return '''The recommendation for the sodium was not computed. Did you put in all the information to 
		have a recommendation ?'''


def Fruits_text(Fruits_ratio):
	''' Return text of the feedback for fruits/vegs/nuts intake

	Input:
	Fruit_ratio(float): Percentage of fruits/vegetables/nuts in the total mass of consumed food

	Output:
	(str): Feedback on fruits/vegs/nuts intake
	'''

	return 'Your menu is composed of {:.1f} % of fruits, vegetables and/or nuts.'.format(Fruits_ratio)


def Rec_text(Male, Age, Exercice, Days, Weight, Dict_):
	'''Main function to assemble the text for the various feedbacks

	Input:
	Male(bool): True if the user is male, false if the user is female
	Age(int): Age of the user
	Exercice(float): Level of activity of the user (1.4 = static, 1.6 = average, 1.8 = active)
	Days(int): Number of days in which these proteins were consumed
	Weight(int/float): Weight of the user (in kg)
	Dict_(dictionary): Contains the total quantities consumed (or ratio) for each nutrient
	
	Output:
	(str): Global feedback on nutrients intake
	'''

	# Total quantities consumed, for each nutrient
	Energy_quantites = Dict_['Energy']
	Lipid_quantites = Dict_['Fat']
	Protein_quantites = Dict_['Protein']
	Beverages_quantites = Dict_['Beverages_quantites']
	Fiber_quantites = Dict_['Fiber']
	Sugar_quantites = Dict_['Sugar']
	Sodium_quantites = Dict_['Sodium']
	Soda_ratio = Dict_['Soda_ratio']
	Fruits_ratio = Dict_['Fruits']

	# Get feedback texts for each nutrient 
	Energy = Energy_text(Male, Exercice, Age, Energy_quantites, Days)
	Lipid = Lipid_text(Age, Lipid_quantites, Energy_quantites)
	Prot = Prot_text(Male, Age, Protein_quantites, Weight, Days)
	Water = Water_text(Beverages_quantites, Soda_ratio, Days, Age)
	Fiber = Fiber_text(Fiber_quantites, Days)
	Sugar = Sugar_text(Sugar_quantites, Days)
	Sodium = Sodium_text(Age, Sodium_quantites, Days)
	Fruits = Fruits_text(Fruits_ratio)

	# Format feedback texts
	text = '<h2 style="color:#3C627E"> Recommendation </h2>'
	text_energy = '<h3 style="color:#008080">Energy</h3>' + Energy
	text_lipid = '<h3 style="color:#008080">Lipid</h3>' + Lipid
	text_prot = '<h3 style="color:#008080">Protein</h3>' + Prot
	text_water = '<h3 style="color:#008080">Water</h3>' + Water
	text_fiber = '<h3 style="color:#008080">Fiber</h3>' + Fiber
	text_sugar = '<h3 style="color:#008080">Sugar</h3>' + Sugar
	text_sodium = '<h3 style="color:#008080">Sodium</h3>' + Sodium
	text_fruits = '<h3 style="color:#008080">Fruits - Vegetables - Nuts</h3>' + Fruits

	# Append conclusion
	text_end = '''<h4 style="color:#3C627E">Information</h4><p>The recommendation was computed according to the
	<a href="http://www.sge-ssn.ch/fr/science-et-recherche/denrees-alimentaires-et-nutriments/recommandations-nutritionnelles/valeurs-de-reference-dach/" target="_blanck"
	>Société Suisse de Nutrition (SSN)</a> reference values [in French/Deutch/Italian]. We do not provide any additional information
	regarding vitamins or additives. For vitamins, you can check out the SSN website. Concerning the additives that may be found in your products,
	we suggest you to see <a href="https://pages.rts.ch/emissions/abe/1371092-liste-des-principaux-additifs-alimentaires.html" target="_blanck">
	A Bon Entendeur (RTS) [in French]</a>. Also, if you are pregnant or an athlete, other recommendations may apply.
	These recommendations are not for medical use and have been computed from <a href="https://world.openfoodfacts.org/" target="_blanck">
	Open Food Facts</a> database.</p>'''

	return text + text_energy + text_sugar + text_lipid + text_prot + text_fruits + text_fiber + text_sodium + text_water + text_end
	


