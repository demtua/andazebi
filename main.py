from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from DB.db_manager import DB
from screens.game_screen import GameScreen
from screens.menu_screen import MenuScreen
from screens.liderboard_screen import LiderboardScreen
import os
import sys



class HangmanApp(App):
    
    timer_time = NumericProperty(10)


    def build(self):
        self.title = 'ანდაზები'
        self.sm = ScreenManager()
        self.db = DB()

        self.game_screen = GameScreen(name='game_screen')
        self.menu_screen = MenuScreen(name='menu_screen')
        self.liderboard_screen = LiderboardScreen(name='liderboard_screen')
        self.sm.add_widget(self.menu_screen)
        self.sm.add_widget(self.game_screen)
        self.sm.add_widget(self.liderboard_screen)
        return self.sm
    
    def resource_path(self, relative_path):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    

    def on_time_select(self, text):
        if text == "10:00":
            self.timer_time = 600
        elif text == "5:00":
            self.timer_time = 300
        elif text == "3:00":
            self.timer_time = 180



        


  


HangmanApp().run()