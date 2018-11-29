from kivy.app import App

from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('manager.kv')
Builder.load_file('screenhome.kv')
Builder.load_file('screenproduct.kv')
Builder.load_file('screenquantities.kv')

import pandas as pd

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