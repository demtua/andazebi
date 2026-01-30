from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from DB.db_manager import DB
from screens.game_screen import GameScreen
from screens.menu_screen import MenuScreen
from screens.liderboard_screen import LiderboardScreen
from kivy.clock import Clock
import os
import sys
from kivy.lang import Builder
from firebase import OnlineLeaderboard

def get_kv_path(filename):
    # 1. Check if we are running as a bundled EXE
    if hasattr(sys, '_MEIPASS'):
        # Check root of EXE
        path = os.path.join(sys._MEIPASS, filename)
        if os.path.exists(path):
            return path
    
    # 2. Check the 'screens' folder (Development mode)
    dev_path = os.path.join('screens', filename)
    if os.path.exists(dev_path):
        return dev_path
        
    # 3. Fallback to just the filename in current dir
    return filename

# Now load it safely
Builder.load_file(get_kv_path('menu_screen.kv'))
class HangmanApp(App):
    
    timer_time = NumericProperty(5)
    

    def build(self):
        self.title = 'ანდაზები'
        self.sm = ScreenManager()
        self.db = DB()
        self.times = {
            "10:00":600,
            "5:00":300,
            "3:00":180
        }
        self.online_liderboard = OnlineLeaderboard()
        self.start_sync()
        Clock.schedule_once(lambda x: self.get_time_choice(),0)
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
        
        self.timer_time = self.times[text] 
        Clock.schedule_once(lambda x: self.db.update_time_choice(self.timer_time))



    def get_time_choice(self):
        self.timer_time = self.db.get_time_choice()
        print(self.timer_time)
        x = [key for key, value in self.times.items() if self.timer_time == value ]
        try:
            self.menu_screen.timer.text = x[0] 
        except:
            self.menu_screen.timer.text =  "10:00"

    def start_sync(self):
        unsynced = self.db.get_unsynced_scores() # From your Local DB manager
        for row in unsynced:
            name, score, time = row
            # We pass the local DB function as the callback
            self.online_liderboard.sync_score(name, score, time, self.db.mark_as_synced)
  


HangmanApp().run()