# Import kivy tools
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

# Import the kv files
Builder.load_file('./src/rv.kv')
Builder.load_file('./src/screenhome.kv')
Builder.load_file('./src/screenprofile.kv')
Builder.load_file('./src/screensettings.kv')
Builder.load_file('./src/screenproduct.kv')
Builder.load_file('./src/screenquantities.kv')
Builder.load_file('./src/screenfinal.kv')
Builder.load_file('./src/manager.kv')

# Other imports
import pandas as pd
import re
from Algo_main import algo # Import the algorithm for NutriScore computation

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Add selection and focus behaviour to the view '''
    pass

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
        ''' Respond to the selection of items '''

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
    ''' Class for the RecycleView Controller '''

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def upload(self, query, active):
        ''' Search data according to the user input '''

        # Reset data
        self.data = []

        # Check if the Raw Food CheckBox is active or not
        if active:
            self.parent.parent.getSelection('API', query, True)
            self.data = [{'label1': {'text': 'API'}, 'label2': {'text': query}, 'label3': {'text': 'Add/Remove'}}]
            
        else:
            isinside = allTrue
            for item in query.split(): # Split the query in keywords
                isinside = isinside & \
                    (DF['product_name'].str.contains(item, case=False) | \
                    DF['Brands'].str.contains(item, case=False))

            if any(isinside):
                selection = DF[isinside] # Select products to display
                
                for row in selection.itertuples(): # Iterate through the columns of DF
                    d = {'label1': {'text': str(row[0])}, \
                        'label2': {'text': str(row[1])},
                        'label3': {'text': str(row[-1])}} # barcode, product_name, brand
                    self.data.append(d)
            else:
                isinside = DF.index.str.contains(query, case=False) # Search for Barcode

                if any(isinside):
                    selection = DF[isinside]

                    for row in selection.itertuples():
                        d = {'label1': {'text': str(row[0])}, \
                            'label2': {'text': str(row[1])},
                            'label3': {'text': str(row[-1])}} # barcode, product_name, brand
                        self.data.append(d)  

                else:
                    # In case no product is found
                    self.data = [{'label1': {'text': ''}, \
                        'label2': {'text': 'No product found'}, 'label3': {'text': ''}}]
    def getQuantities(self, dict):
        ''' Gather data for display on Quantities Screen '''

        self.data = []
        code = dict['code']
        product_name = dict['product_name']
        quantity = dict['quantity']

        for index in range(len(code)):
            d = {'label1': {'text': code[index]}, 'label2': {'text': product_name[index]}, \
                'label3': {'text': quantity[index]}}
            self.data.append(d)

class ScreenHome(Screen):
    ''' Class for the Home Screen. No variables or functions needed for this screen '''
    pass

class ScreenProfile(Screen):
    ''' Class for the Profile Screen '''

    def updateDF(self):
        global DF
        DF = pd.read_csv('https://drive.google.com/uc?export=download&id=1aLUh1UoQcS9lBa6oVRln-DuskxK5uK3y', \
                              index_col=[0], low_memory = False)

        DF.to_csv('./data/OpenFoodFacts_final.csv.gz', compression='gzip')
        self.ids['update'].text = 'Updated'
        self.ids['update'].background_color = (0,1,0,1)

    def update(self):
        self.ids['update'].text = 'Updating'
        self.ids['update'].background_color = (50/255,164/255,206/255,1)        


class ScreenSettings(Screen):
    ''' Class for the Settings Screen '''

    settings = {'rec': True,'name': '', 'surname': '', 'age': 0, 'sex': True, 'weight': 0, \
            'email': '', 'activity': 0, 'days': 0}
    id_profile = -999

    def resetForm(self):
        ''' Reset the indicators of invalid input '''

        self.ids.sex.color = (1,1,1,1)
        self.ids.activity.color = (1,1,1,1)
        self.ids.age.hint_text_color = (0.5, 0.5, 0.5, 1.0)
        self.ids.weight.hint_text_color = (0.5, 0.5, 0.5, 1.0)
        self.ids.days.hint_text_color = (0.5, 0.5, 0.5, 1.0)
        self.ids.email.hint_text_color = (0.5, 0.5, 0.5, 1.0)
        self.ids.name.hint_text_color = (0.5, 0.5, 0.5, 1.0)
        self.ids.surname.hint_text_color = (0.5, 0.5, 0.5, 1.0)

    def setForm(self, id_profile):
        self.id_profile = id_profile
        self.settings = {'rec': True,'name': '', 'surname': '', 'age': 0, 'sex': True, 'weight': 0, \
            'email': '', 'activity': 0, 'days': 0}

        if int(self.id_profile) >= 0:
            self.ids.name.text = str(profile_list.iloc[self.id_profile]['name'])
            self.ids.surname.text= str(profile_list.iloc[self.id_profile]['surname'])
            self.ids.age.text = str(profile_list.iloc[self.id_profile]['age'])
            if bool(profile_list.iloc[self.id_profile]['sex']):
                self.ids.male.active = True
                self.ids.female.active = False

            else:
                self.ids.male.active = False
                self.ids.female.active = True

            self.ids.weight.text = str(profile_list.iloc[self.id_profile]['weight'])
            self.ids.email.text = str(profile_list.iloc[self.id_profile]['email'])
            self.ids.days.text = str(profile_list.iloc[self.id_profile]['days'])
            if int(profile_list.iloc[self.id_profile]['activity']) == 1.8:
                self.ids.seated.active = False
                self.ids.both.active = False
                self.ids.standing.active = True

            elif int(profile_list.iloc[self.id_profile]['activity']) == 1.6:
                self.ids.seated.active = False
                self.ids.both.active = True
                self.ids.standing.active = False

            else:
                self.ids.seated.active = True
                self.ids.both.active = False
                self.ids.standing.active = False
        elif int(self.id_profile) == -999:
            self.ids.name.text = ''
            self.ids.surname.text = ''
            self.ids.age.text = ''
            self.ids.male.active = False
            self.ids.female.active = False
            self.ids.email.text = ''
            self.ids.weight.text = ''
            self.ids.seated.active = False
            self.ids.both.active = False
            self.ids.standing.active = False
            self.ids.days.text = ''
        else:
            self.changeScreen(False)

    def changeScreen(self, valid):
        ''' Handle the validity of the inputs and the change of current screen '''

        if valid:
            self.resetForm()
            # Check name validity
            if self.ids.name.text.strip() == '':
                self.ids.name.hint_text_color = (1,0,0,1)
                return False
            # Check surname validity
            elif self.ids.surname.text.strip() == '':
                self.ids.surname.hint_text_color = (1,0,0,1)
                return False
            # Check age validity
            elif self.ids.age.text.strip() == '' or int(self.ids.age.text) <= 0 or \
              int(self.ids.age.text) >= 120:
                self.ids.age.text = ''
                self.ids.age.hint_text_color = (1,0,0,1)
                return False
            # Check sex validity
            elif not(self.ids.male.active or self.ids.female.active):
                self.ids.sex.color = (1,0,0,1)  
                return False
            # Check email validity
            elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.ids.email.text):
                self.ids.email.text = ''
                self.ids.email.hint_text_color = (1,0,0,1)
                return False
            # Check weight validity
            elif self.ids.weight.text.strip() == '' or int(self.ids.weight.text) <= 0:
                self.ids.weight.text = ''
                self.ids.weight.hint_text_color = (1,0,0,1)
                return False 
            # Check activity validity
            elif not(self.ids.seated.active or self.ids.both.active or self.ids.standing.active):
                self.ids.activity.color = (1,0,0,1)
                return False
            # Check days validity
            elif self.ids.days.text.strip() == '' or int(self.ids.days.text) <= 0:
                self.ids.days.text = ''
                self.ids.days.hint_text_color = (1,0,0,1)
                return False
            
            else: # Validation of the form and reset
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

                self.resetForm()

        else: # If the user pass the settings screen
            self.settings['rec'] = False

        self.manager.setSettings(self.settings, self.id_profile)
        # Change the current screen
        self.manager.current = 'Product Screen'

class ScreenProduct(Screen):
    ''' Class for the Product Screen '''

    temp_dict = {'code':'', 'product_name': ''}

    def getSelection(self, text1, text2, state):
        # Select or deselect temporarly a product
        if state:
            self.temp_dict['code'] = text1
            self.temp_dict['product_name'] = text2

        else:
            self.temp_dict['code'] = ''
            self.temp_dict['product_name'] = ''

class ScreenQuantities(Screen):
    ''' Class for the Quantities Screen '''

    temp_dict = {'code': [], 'product_name': [], 'quantity': [], 'color': []}

    def initQuantity(self, data):
        ''' Initialize the dictionary of the products '''

        if self.temp_dict['quantity'] == []:
            self.temp_dict = data

        self.ids.rv.getQuantities(data)

    def updateQuantity(self, index, text1, text2, text3): 
        ''' Store the quantities input by the user '''

        l = len(self.temp_dict['quantity'])

        if text3 == '' or text3 == '-' or int(text3) < 0:
            text3 = '0'

        if index < l:
            self.temp_dict['code'][index] = text1
            self.temp_dict['product_name'][index] = text2
            self.temp_dict['quantity'][index] = text3
        
        # Append the list of quantities if needed
        else:
            temp = ['0' for i in range(index-l)] 
            self.temp_dict['code'] = self.temp_dict['code'] + temp + [text1]
            self.temp_dict['product_name'] = self.temp_dict['product_name'] + temp + [text2]
            self.temp_dict['quantity'] = self.temp_dict['quantity'] + temp + [text3]

        # Update the data displayed
        self.initQuantity(self.temp_dict)

class ScreenFinal(Screen):
    ''' Class for the Final Screen. No variables or functions needed for this screen '''
    pass

class Manager(ScreenManager):
    ''' Class for the Manager Controller. Store main data '''
    selected_products = {'code': [], 'product_name': [], 'quantity': []}
    settings = {'Rec': True, 'Name': '', 'Surname': '', 'Email': '', 'Age': 0, 'Sex': True, 'Pal': 0, \
            'Weight': 0, 'Day': 0}

    def getProfiles(self):
        self.ids.screen_profile.ids.profile_spinner.values = \
            [str(index + 1) + ' : ' + str(profile_list['name'][index]) + ' ' + str(profile_list['surname'][index]) \
            for index in profile_list.index]

    def toSettings(self, text):
        if text == 'new':
            id_profile = -999
        elif text == 'pass':
            id_profile = -1000
        else:
            items = text.split()
            id_profile = items[0].strip()
            id_profile = int(id_profile) - 1

        self.ids.screen_settings.setForm(id_profile)
        if id_profile != -1000:
            self.current = 'Settings Screen'
        

    def addProduct(self):
        ''' Add product to main storage '''
        item1 = self.ids.screen_product.temp_dict['code']
        item2 = self.ids.screen_product.temp_dict['product_name']

        if item1 != '' and item2 != '':
            self.selected_products['code'].append(item1)
            self.selected_products['product_name'].append(item2)
            self.selected_products['quantity'].append('0')

    def deleteProduct(self):
        ''' Remove product of main storage '''
        item1 = self.ids.screen_product.temp_dict['code']
        item2 = self.ids.screen_product.temp_dict['product_name']

        if item1 in self.selected_products['code'] and item2 in self.selected_products['product_name']:
            self.selected_products['code'].remove(item1)
            self.selected_products['product_name'].remove(item2)
            self.selected_products['quantity'].pop()

    def getQuantities(self, data):
        ''' Add quantities to main storage '''

        self.selected_products['quantity'] = data['quantity']
        l = len(self.selected_products['quantity'])

        for item in range(l):

            if  self.selected_products['quantity'][item] == '':
                self.selected_products['quantity'][item] = '0'
            
        self.current = 'Final Screen'

    def setSettings(self, data, new):
        ''' Add settings to main storage '''

        self.settings['Rec'] = data['rec']
        self.settings['Name'] = data['name']
        self.settings['Surname'] = data['surname']
        self.settings['Email'] = data['email']
        self.settings['Pal'] = data['activity']
        self.settings['Weight'] = data['weight']
        self.settings['Day'] = data['days']
        self.settings['Sex'] = data['sex']
        self.settings['Age'] = data['age']
        
        update = True

        if new == -999:
            temp_df = pd.DataFrame.from_dict({'index': [len(profile_list)], \
                'name': [data['name']], 'surname': [data['surname']], \
                'age': [data['age']], 'sex': [data['sex']], 'email': [data['email']], \
                'weight': [data['weight']], \
                'activity': [data['activity']], 'days': [data['days']]}).set_index('index')
            new_profile_list = pd.concat([profile_list, temp_df]) 
        elif new == -1000:
            update = False
        else:
            temp_df = pd.DataFrame.from_dict({'name': [data['name']], 'surname': [data['surname']], \
                'age': [data['age']], 'sex': [data['sex']], 'email': [data['email']], 'weight': [data['weight']], \
                'activity': [data['activity']], 'days': [data['days']]})
            new_profile_list= profile_list
            new_profile_list.iloc[new] = temp_df.iloc[0]

        if update:
            new_profile_list.to_csv('./data/profile.csv', sep=';')


    def computation(self):
        ''' Call algo for computation of NutriScore and recommendation. Display results '''
        dict_product = {'Product': [], 'API': []}

        for index in range(len(self.selected_products['code'])):
           
            # Separation of API and OpenFoodFacts data
            if str(self.selected_products['code'][index]) == 'API':
                dict_product['API'].append((str(self.selected_products[
                    'product_name'][index]), int(self.selected_products['quantity'][index])))
           
            else:
                dict_product['Product'].append((str(self.selected_products[
                    'code'][index]), int(self.selected_products['quantity'][index])))

        # Run the algorithm to get the recommendation to print on-screen
        text_app_beverages, text_app_nonbeverages =  algo(dict_product, self.settings, DF)
        self.ids.screen_final.ids.beverages.text = text_app_beverages
        self.ids.screen_final.ids.non_beverages.text = text_app_nonbeverages

class NutriScoreApp(App):
    ''' Main class of the App '''

    def build(self):
        ''' Import the database for the whole application '''
        global DF, allTrue, profile_list

        try:
            DF = pd.read_csv('./data/OpenFoodFacts_final.csv.gz', low_memory=False, index_col = [0])
            allTrue = DF['product_name'].str.contains('', case=False) # True Vector of length len(DF)
            profile_list = pd.read_csv('./data/profile.csv', sep=';', index_col=[0])

        except:
            print('Fatal error: files missing')  
                  
        return Manager()

if __name__ == '__main__':
    NutriScoreApp().run()

