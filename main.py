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
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
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


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

class Grid(GridLayout):
    pass
    # def __init__(self, **kwargs):
    #     df = pd.read_csv('./data/Sample_data_food.csv')
    #     for heading in df.columns:
    #         self.add_widget(Label(text=heading))

class RV(RecycleView):
    grid = RecycleGridLayout
    df = pd.read_csv('../data/data_food_final.csv')
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def upload(self, query, active):
        self.data = []
        if active:
            pass
        else:
            isinside = self.df['product_name'].str.contains('', case=False)
            for item in query.split():
                isinside = isinside & self.df['product_name'].str.contains(item, case=False)
            if any(isinside):
                selection = self.df[isinside]
                self.data = [{'text': str(row[1]) + '  -  ' +str(row[2]), 'font_size': 20} for row in selection.itertuples()]
            else:
                isinside = self.df['code'].str.match(query, case=False)
                if any(isinside):
                    selection = self.df[isinside]
                    self.data = [{'text': str(row[1]) + '  -  ' +str(row[2]), 'font_size': 20} for row in selection.itertuples()]
                else:
                    self.data = [{'text' : 'No product found'}]

class ScreenHome(Screen):
    pass

class ScreenProduct(Screen):
    pass

class ScreenQuantities(Screen):
    pass

class Manager(ScreenManager):
    pass

class NutriScoreApp(App):
    def build(self):
        return Manager()

if __name__ == '__main__':
    NutriScoreApp().run()