from kivy.uix.screenmanager import Screen
from kivy.app import App
from DB.db_manager import DB
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class LiderboardScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.db = DB()
        self.board_grid = Board()
        self.add_widget(self.board_grid)


    def get_liderboard(self):
        data = self.db.get_liderboard()
        return data

    def on_enter(self, *args):
        data = self.get_liderboard()
        # print(data)
        self.board_grid.populate(data)
        # Clock.schedule_once(lambda x:,2)

from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp

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
            text="← Back",
            size_hint_x=None,
            width=dp(100)
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
            self.rows.add_widget(Label(text="No scores yet"))
            self.rows.add_widget(Label(text=""))
            self.rows.add_widget(Label(text=""))
            return

        for score, name, play_time in data:
            self.rows.add_widget(Label(text=str(name), halign="left"))
            self.rows.add_widget(Label(text=str(score)))
            self.rows.add_widget(Label(text=str(play_time)))