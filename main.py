from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout

Builder.load_file('manager.kv')
Builder.load_file('screenhome.kv')
Builder.load_file('screenproduct.kv')
Builder.load_file('screenquantities.kv')
Builder.load_file('rv.kv')

import pandas as pd

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableGrid(RecycleDataViewBehavior, GridLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids['id_label1'].text = data['label1']['text']
        self.ids['id_label2'].text = data['label2']['text']
        self.ids['id_label3'].text = data['label3']['text']
        return super(SelectableGrid, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableGrid, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

class SelectableQuantity(RecycleDataViewBehavior, GridLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        self.ids['id_label1'].text = data['label1']['text']
        self.ids['id_label2'].text = data['label2']['text']
        return super(SelectableQuantity, self).refresh_view_attrs(
            rv, index, data)

class RV(RecycleView):
    
    df = pd.read_csv('../data/OpenFoodFacts_final.csv', low_memory=False)
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def upload(self, query, active):
        self.data = []
        if active:
            pass
        else:
            isinside = self.df['product_name'].str.contains('', case=False)
            for item in query.split():
                isinside = isinside & \
                    (self.df['product_name'].str.contains(item, case=False) | \
                    self.df['Brands'].str.contains(item, case=False))
            if any(isinside):
                selection = self.df[isinside]
                self.data = []
                for row in selection.itertuples():
                    d = {'label1': {'text': str(row[1])}, \
                        'label2': {'text': str(row[2])},
                        'label3': {'text': str(row[-1])}}
                    self.data.append(d)
            else:
                isinside = self.df['code'].str.contains(query, case=False)
                if any(isinside):
                    selection = self.df[isinside]
                    for row in selection.itertuples():
                        d = {'label1': {'text': str(row[1])}, \
                            'label2': {'text': str(row[2])},
                            'label3': {'text': str(row[-1])}}
                        self.data.append(d)                
                else:
                    self.data = [{'label1': {'text': ''}, \
                        'label2': {'text': 'No product found'}, 'label3': {'text': ''}}]
    
    def getQuantities(self, dict):
        self.data = []
        code = dict['code']
        product_name = dict['product_name']
        for index in range(len(code)):
            d = {'label1': {'text': code[index]}, 'label2': {'text': product_name[index]}, 'label3': {'text': ''}}
            self.data.append(d)

class ScreenHome(Screen):
    pass

class ScreenProduct(Screen):
    temp_dict = {'code':'', 'product_name': ''}
    def getSelection(self, text1, text2, state):
        if state:
            self.temp_dict['code'] = text1
            self.temp_dict['product_name'] = text2
        else:
            self.temp_dict['code'] = ''
            self.temp_dict['product_name'] = ''

class ScreenQuantities(Screen):
    def getSelection(self, text, state):
        if state:
            pass    

class Manager(ScreenManager):
    selected_products = {'code': [], 'product_name': [], 'quantity': []} 

    def addProduct(self):
        item1 = self.ids.screen_product.temp_dict['code']
        item2 = self.ids.screen_product.temp_dict['product_name']
        if item1 != '' and item2 != '':
            self.selected_products['code'].append(item1)
            self.selected_products['product_name'].append(item2)
        print(self.selected_products)

    def deleteProduct(self):
        item1 = self.ids.screen_product.temp_dict['code']
        item2 = self.ids.screen_product.temp_dict['product_name']
        if item1 in self.selected_products['code'] and item2 in self.selected_products['product_name']:
            self.selected_products['code'].remove(item1)
            self.selected_products['product_name'].remove(item2)
        print(self.selected_products)

class NutriScoreApp(App):
    def build(self):
        return Manager()

if __name__ == '__main__':
    NutriScoreApp().run()