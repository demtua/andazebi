from kivy.uix.screenmanager import Screen
from kivy.app import App
from DB.db_manager import DB
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from firebase import OnlineLeaderboard

class LiderboardScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.db = DB()
        self.board_grid = Board()
        self.add_widget(self.board_grid)
        self.online_liderboard = OnlineLeaderboard()


    def get_liderboard(self):
        self.online_liderboard = OnlineLeaderboard()
        
        # We do NOT assign to a variable. 
        # We just "fire and forget" and let process_data handle the result later.
        self.online_liderboard.fetch_scores(self.process_data)
        
        print("Fetch started... but data isn't here yet!")

    def on_enter(self, *args):
        # Just start the process. Don't try to use 'data' here.
        self.get_liderboard()

    def get_liderboard(self):
        self.online_liderboard = OnlineLeaderboard()
        self.online_liderboard.fetch_scores(self.process_data)

    def process_data(self, data):
        if data is None:
            print("Failed to get data.")
            return

        # 1. Convert dict to a list and sort it (Highest score first)
        leaderboard_list = list(data.values())
        leaderboard_list.sort(key=lambda x: int(x.get('score', 0)), reverse=True)

        # 2. NOW update the UI
        # Since this function runs when the data arrives, 
        # the grid will fill up automatically!
        self.board_grid.populate(leaderboard_list)
        print("UI populated with fetched data.")





from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
import os
import sys

def resource_path( relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# ---------- Helper ----------
def make_label(text, align="center"):
    lbl = Label(
        text=str(text),
        halign=align,
        valign="middle"
    )
    lbl.bind(size=lbl.setter("text_size"))
    return lbl


class Board(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = dp(10)
        self.spacing = dp(6)

        # ===== TOP BAR =====
        top_bar = BoxLayout(size_hint_y=None, height=dp(40))

        back_btn = Button(
            text="Back",
            size_hint=(None,None),
            background_normal=resource_path('assets/timer.png'),
            size=(dp(100), dp(65)),
            pos_hint={"top":1}
        )
        back_btn.bind(on_release=self.go_back)

        top_bar.add_widget(back_btn)
        top_bar.add_widget(Label())  # spacer

        self.add_widget(top_bar)

        # ===== HEADER =====
        header = GridLayout(cols=3, size_hint_y=None, height=dp(40))
        header.add_widget(Label(text="[b]Name[/b]", markup=True, halign="left"))
        header.add_widget(Label(text="[b]Score[/b]", markup=True, halign="center"))
        header.add_widget(Label(text="[b]Time[/b]", markup=True, halign="center"))

        self.add_widget(header)

        # ===== SCROLL AREA =====
        scroll = ScrollView()

        self.rows = GridLayout(
            cols=3,
            size_hint_y=None,
            row_default_height=dp(36),
            row_force_default=True,
            spacing=dp(4)
        )
        self.rows.bind(minimum_height=self.rows.setter("height"))

        scroll.add_widget(self.rows)
        self.add_widget(scroll)

    def go_back(self, *args):
        App.get_running_app().sm.switch_to(App.get_running_app().menu_screen)

    def populate(self, data):
        self.rows.clear_widgets()

        if not data:
            # Fill the row so it doesn't look empty
            for _ in range(3):
                self.rows.add_widget(Label(text="--", font_name=resource_path('assets/BPG2.ttf')))
            return

        # Dictionary to map seconds to display strings
        times_map = {
            "600": "10:00",
            "300": "5:00",
            "180": "3:00"
        }

        for entry in data:
            # Extract values from the dictionary safely
            name = entry.get('name', 'Unknown')
            score = entry.get('score', 0)
            play_time_raw = str(entry.get('time', ''))

            # Get formatted time from map, or use the raw value if not found
            display_time = times_map.get(play_time_raw, play_time_raw)
            
            # Add widgets to the grid
            self.rows.add_widget(Label(text=str(name), halign="left", font_name=resource_path('assets/BPG2.ttf')))
            self.rows.add_widget(Label(text=str(score), font_name=resource_path('assets/BPG2.ttf')))
            self.rows.add_widget(Label(text=display_time, font_name=resource_path('assets/BPG2.ttf')))