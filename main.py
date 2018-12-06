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
Builder.load_file('screensettings.kv')
Builder.load_file('screenfinal.kv')

import pandas as pd
import re
from Algo_main import algo

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
        self.ids['id_label3'].text = data['label3']['text']
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
        quantity = dict['quantity']
        for index in range(len(code)):
            d = {'label1': {'text': code[index]}, 'label2': {'text': product_name[index]}, \
                'label3': {'text': quantity[index]}}
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
    temp_dict = {'code': [], 'product_name': [], 'quantity': []}

    def initQuantity(self, data):
        if self.temp_dict['quantity'] == []:
            self.temp_dict = data

        self.ids.rv.getQuantities(data)

    def updateQuantity(self, index, text1, text2, text3):
        l = len(self.temp_dict['quantity'])
        if index < l:
            self.temp_dict['code'][index] = text1
            self.temp_dict['product_name'][index] = text2
            self.temp_dict['quantity'][index] = text3
        else:
            temp = ['0' for i in range(index-l)]
            self.temp_dict['code'] = self.temp_dict['code'] + temp + [text1]
            self.temp_dict['product_name'] = self.temp_dict['product_name'] + temp + [text2]
            self.temp_dict['quantity'] = self.temp_dict['quantity'] + temp + [text3]


class ScreenSettings(Screen):
    settings = {'rec': True,'name': '', 'surname': '', 'age': 0, 'sex': True, 'weight': 0, \
            'email': '', 'activity': 0, 'days': 0}

    def changeScreen(self, valid):
        if valid:
            if self.ids.name.text.strip() == '' and self.ids.name.text != 'Invalid name':
                self.ids.name.text = 'Invalid name'
                self.ids.name.foreground_color = (1,0,0,1)
                self.ids.name.hint_text_color = (1,0,0,1)
                return False
            elif self.ids.surname.text.strip() == '' and self.ids.surname.text != 'Invalid surname':
                self.ids.surname.text = 'Invalid surname'
                self.ids.surname.foreground_color = (1,0,0,1)
                self.ids.surname.hint_text_color = (1,0,0,1)
                return False
            elif self.ids.age.text.strip() == '' or int(self.ids.age.text) <= 0 or \
              int(self.ids.age.text) >= 120:
                self.ids.age.color = (1,0,0,1)
                self.ids.age.hint_text_color = (1,0,0,1)
                return False
            elif not(self.ids.male.active or self.ids.female.active):
                self.ids.sex.color = (1,0,0,1)  
                self.ids.sex.hint_text_color = (1,0,0,1) 
                return False
            elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.ids.email.text):
                self.ids.email.text = 'Invalid email'
                self.ids.email.foreground_color = (1,0,0,1)
                self.ids.email.hint_text_color = (1,0,0,1)
                return False
            elif self.ids.weight.text.strip() == '' or int(self.ids.weight.text) <= 0:
                self.ids.weight.color = (1,0,0,1)
                self.ids.weight.hint_text_color = (1,0,0,1)
                return False 
            elif not(self.ids.seated.active or self.ids.both.active or self.ids.standing.active):
                self.ids.activity.color = (1,0,0,1)
                self.ids.activity.hint_text_color = (1,0,0,1)
                return False
            elif self.ids.days.text.strip() == '' or int(self.ids.days.text) <= 0:
                self.ids.days.color = (1,0,0,1)
                self.ids.days.hint_text_color = (1,0,0,1)
                return False
            else:    
                self.settings['rec'] = True
                self.settings['name'] = self.ids.name.text
                self.settings['surname'] = self.ids.surname.text
                self.settings['age'] = int(self.ids.age.text)
                self.settings['weight'] = int(self.ids.weight.text)
                self.settings['email'] = self.ids.email.text
                self.settings['days'] = int(self.ids.days.text)
                self.settings['sex'] = self.ids.male.active
                if self.ids.seated.active:
                    self.settings['activity'] = 1.4
                if self.ids.both.active:
                    self.settings['activity'] = 1.6
                if self.ids.standing.active:
                    self.settings['activity'] = 1.8
                self.ids.sex.color = (1,1,1,1)
                self.ids.age.color = (1,1,1,1)
                self.ids.weight.color = (1,1,1,1)
                self.ids.activity.color = (1,1,1,1)
                self.ids.days.color = (1,1,1,1)
                self.ids.sex.hint_text_color = (0.5, 0.5, 0.5, 1.0)
                self.ids.age.hint_text_color = (0.5, 0.5, 0.5, 1.0)
                self.ids.weight.hint_text_color = (0.5, 0.5, 0.5, 1.0)
                self.ids.activity.hint_text_color = (0.5, 0.5, 0.5, 1.0)
                self.ids.days.hint_text_color = (0.5, 0.5, 0.5, 1.0)
                self.ids.email.foreground_color = (1,1,1,1)
                self.ids.email.hint_text_color = (0.5, 0.5, 0.5, 1.0)
                self.ids.name.foreground_color = (1,1,1,1)
                self.ids.name.hint_text_color = (0.5, 0.5, 0.5, 1.0)
                self.ids.surname.foreground_color = (1,1,1,1)
                self.ids.surname.hint_text_color = (0.5, 0.5, 0.5, 1.0)

        else:
            self.settings['rec'] = False
        self.manager.setSettings(self.settings)
        self.manager.current = 'Final Screen'

class ScreenFinal(Screen):
    pass

class Manager(ScreenManager):
    selected_products = {'code': [], 'product_name': [], 'quantity': []}
    settings = {'Rec': True, 'Name': '', 'Surname': '', 'Email': '', 'Age': 0, 'Sex': True, 'Pal': 0, \
            'Weight': 0, 'Day': 0}
    df = pd.read_csv('../data/OpenFoodFacts_final.csv', low_memory=False, index_col = [0])

    def addProduct(self):
        item1 = self.ids.screen_product.temp_dict['code']
        item2 = self.ids.screen_product.temp_dict['product_name']
        if item1 != '' and item2 != '':
            self.selected_products['code'].append(item1)
            self.selected_products['product_name'].append(item2)
            self.selected_products['quantity'].append('0')

    def deleteProduct(self):
        item1 = self.ids.screen_product.temp_dict['code']
        item2 = self.ids.screen_product.temp_dict['product_name']
        if item1 in self.selected_products['code'] and item2 in self.selected_products['product_name']:
            self.selected_products['code'].remove(item1)
            self.selected_products['product_name'].remove(item2)
            self.selected_products['quantity'].pop()

    def getQuantities(self, data):
        
        self.selected_products['quantity'] = data['quantity']
        l = len(self.selected_products['quantity'])
        for item in range(l):
            if  self.selected_products['quantity'][item] == '':
                self.selected_products['quantity'][item] = '0'
            
        print(self.selected_products)
        self.current = 'Settings Screen'

    def setSettings(self, data):
        self.settings['Rec'] = data['rec']
        self.settings['Name'] = data['name']
        self.settings['Surname'] = data['surname']
        self.settings['Email'] = data['email']
        self.settings['Pal'] = data['activity']
        self.settings['Weight'] = data['weight']
        self.settings['Day'] = data['days']
        self.settings['Sex'] = data['sex']
        self.settings['Age'] = data['age']

    def computation(self):
        dict_product = {'Product': [(str(self.selected_products['code'][index]), \
            int(self.selected_products['quantity'][index])) \
                for index in range(len(self.selected_products['code']))], 'API': []}
        score_beverages, score_nonbeverages =  algo(dict_product, self.settings, self.df)
        self.ids.screen_final.ids.beverages.text = score_beverages
        self.ids.screen_final.ids.non_beverages.text = score_nonbeverages

class NutriScoreApp(App):

    def build(self):
        return Manager()

if __name__ == '__main__':
    NutriScoreApp().run()