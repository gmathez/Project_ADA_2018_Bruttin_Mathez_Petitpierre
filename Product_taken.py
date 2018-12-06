import pandas as pd 

def product_list(list_product, df, list_api):
	text = '<h2 style="color:#3C627E"> Products Selected </h2>'

	if len(list_product) > 0:
		for barcode, quantites in list_product:
			text = text + '''<p>Product : <a href="https://world.openfoodfacts.org/product/{}" target="_blank">{}</a>
			| Quantites : {} [gr/ml]</p>'''.format(barcode, df.loc[barcode]['product_name'], quantites)

	if len(list_api) > 0:
		for nom, quantites in list_api:
			text = text + '''<p>Product : {} | Quantites : {} [gr/ml]</p>'''.format(nom, quantites)

	return text