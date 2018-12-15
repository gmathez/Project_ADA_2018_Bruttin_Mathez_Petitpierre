# Import
import pandas as pd 

def product_list(list_product, df, list_api):
	''' Return text with the product selected by the user

		Inputs:
		list_product(list of tuple[0](str)): Barcodes of the products
		list_product(list of tuple[1](int)): Quantities associated with those products
		df(pandas dataframe): Dataframe containing all products
		list_api(tuple[0](str)): Name of the products to fill from the API
		list_api(tuple[1](int)): Quantities associated with those products

		Output:
		text(str): Text listing the products entered by the user
	'''
	text = '<h2 style="color:#3C627E"> Selected Products</h2>'

	if len(list_product) > 0:
		for barcode, quantites in list_product:
			text = text + '''<p>Product : <a href="https://world.openfoodfacts.org/product/{}" target="_blank">{}</a>
			| Quantities : {} [gr/ml]</p>'''.format(barcode, df.loc[barcode]['product_name'], quantites)

	if len(list_api) > 0:
		for nom, quantites in list_api:
			text = text + '''<p>Product : {} | Quantities : {} [gr/ml]</p>'''.format(nom, quantites)

	return text